# !/user/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import sys
import time
import traceback

import requests
import simplejson as json

import make_pdf
from constants import *
from utils.common import mkdir_p
from utils.logger import get_logger

logger = get_logger(__name__)


def run_parallel(candidates, target, semester):
    # Determine pool size
    nb_cpus = multiprocessing.cpu_count()
    pool_size = (nb_cpus - 1) * 2
    if pool_size == 0:
        pool_size = 2
    # create thread POOL w.r.t the number of available cpus
    pool = multiprocessing.Pool(pool_size)
    logger.info('Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (nb_cpus, pool_size))

    start_time = time.time()

    # assign pdf build tasks to pool
    heading_csv = FIELD_NAMES
    task_args = [(target, idx, candidates[idx], heading_csv, semester) for idx in range(len(candidates))]
    apply_objects = [pool.apply_async(make_pdf.buildPdf, arg) for arg in task_args]

    # wait for execution end
    for r in apply_objects:
        try:
            pdfname = r.get()
        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.error(trace_back)
            logger.error(e)

    pool.close()
    pool.join()

    logger.info('Việc tạo pdf được tiến hành trong %0.2f giây' % (time.time() - start_time))


def run(candidates, target, semester):
    heading_csv = make_pdf.FIELD_NAMES

    for index in range(len(candidates)):
        try:
            make_pdf.buildPdf(target, index, candidates[index], heading_csv, semester)
        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.info(trace_back)
            logger.error(e)
            continue


def get_submissions_from_api(form_id):
    PAGE_SIZE = 100
    candidates = []
    url = URL_SUBMISSION_FORMAT.format(form_id)
    count = get_submission_count(form_id)
    data = {
        'apiKey': API_KEY,
        'pageSize': PAGE_SIZE,
        'sort': "ASC"  # sort oldest to newest
    }
    num_page = int(count / PAGE_SIZE + 1)
    for i in range(num_page):
        data['pageNr'] = i
        response = requests.post(url, data=data)
        res_dict = json.loads(response.content.decode('utf-8'))
        for candidate in res_dict['submissions']:
            candidate_string_list = []
            for field in candidate['fields']:
                candidate_string_list += [field['fieldvalue']]
            candidates += [candidate_string_list]
    return candidates


def get_submission_count(form_id):
    url = URL_SUBMISSION_COUNT_FORMAT.format(form_id, API_KEY)
    response = requests.get(url)
    res_obj = json.loads(response.content)
    submission_count = int(res_obj['submissionsCount'])
    logger.info(f"Tổng số hồ sơ: {submission_count}")
    return submission_count


def create_output_folders(region):
    mkdir_p(OUTPUT_FOLDER)
    mkdir_p(os.path.join(OUTPUT_FOLDER, region))

    os.chdir(os.path.join(OUTPUT_FOLDER, region))
    mkdir_p("tmp")

    for code in SCHOOL_CODE[region].values():
        mkdir_p(code)
        mkdir_p(code + "/DISQUALIFIED")
        mkdir_p("INTERVIEW")
        mkdir_p("INTERVIEW/" + code)


def get_fields(form_id):
    fields = []
    url = URL_FIELDS_FORMAT.format(form_id)
    data = {
        'apiKey': API_KEY
    }
    response = requests.post(url, data=data)
    fields_response = json.loads(response.content.encode('utf-8'))
    for field in fields_response['fields']:
        fields += [field['fieldTitle']]
    with open("fields.json", "w") as fo:
        json.dump(fields, fo)
    return fields


if __name__ == '__main__':
    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--form', dest='form', type=str,
                        help='Choose form to get submissions. Available choice: fr, sg, tw')
    parser.add_argument('-s', '--semester', dest='semester', type=int,
                        help='Current semester')
    parser.add_argument('-l', '--local', dest='use_local', default=False, action='store_true',
                        help='Use local json file')
    args = parser.parse_args()
    form_id = FORM_ID[args.form]

    create_output_folders(args.form)

    if args.form in FORM_ID:
        form_id = FORM_ID[args.form]
        if os.path.exists("{}.json".format(args.form)) and args.use_local:
            with open("{}.json".format(args.form), "r", encoding='utf-8') as f:
                logger.info(f"Loading list of candidates from local file {args.form}.json")
                candidates = json.load(f)
        else:
            logger.info(f"Downloading the list of candidates...")
            candidates = get_submissions_from_api(form_id)
            with open(f"{args.form}.json", "a") as output:
                json.dump(candidates, output)
                logger.info(f"Saving remote data to {args.form}.json")
        run_parallel(candidates, os.path.join(OUTPUT_FOLDER, args.form), args.semester)
    else:
        logger.info("Please choose a form to get submission. Available choice: fr, sg, tw.")
        sys.exit(1)

    logger.info("Done.")
