from lxml import etree
import pandas as pd
import os
from copy import deepcopy
import gc
import multiprocessing as mp


def csv_writer(data, out_file, column_list):
    pd.DataFrame(data).to_csv(out_file, columns=column_list, header=False, index=False, mode='a')


def file_processor(source_file, out_path, site):
    answer_list = []
    question_list = []
    out_path_question = os.path.join(out_path, site + '_q.csv')
    out_path_answer = os.path.join(out_path, site + '_a.csv')
    answer_column_list = ['Site', 'Id', 'PostTypeId', 'ParentId', 'CreationDate', 'Score', 'OwnerUserId']
    question_column_list = ['Site', 'Id', 'PostTypeId', 'CreationDate', 'Score', 'ViewCount', 'OwnerUserId',
                            'Tags', 'AnswerCount', 'AcceptedAnswerId']

    FLUSH_LENGTH = 50_000

    for event, element in etree.iterparse(source_file, tag="row"):

        element.attrib['Site'] = site

        del element.attrib['Body']
        del element.attrib['LastActivityDate']
        del element.attrib['CommentCount']

        try:
            del element.attrib['LastEditDate']
            del element.attrib['LastEditorUserId']
        except KeyError:
            pass

        try:
            del element.attrib['Title']
        except KeyError as e:
            pass
        # if 'ParentId' not in element.attrib:
        #     element.attrib['ParentId'] = ''
        if element.attrib['PostTypeId'] == '1':
            question_list.append(deepcopy(element.attrib))
            if question_list.__len__() >= FLUSH_LENGTH:
                csv_writer(question_list, out_path_question, question_column_list)
                question_list = []
                gc.collect()
        else:
            answer_list.append(deepcopy(element.attrib))
            if answer_list.__len__() >= FLUSH_LENGTH:
                csv_writer(answer_list, out_path_answer, answer_column_list)
                answer_list = []
                gc.collect()
        # print(element.attrib)

        element.clear()
    csv_writer(question_list, out_path_question, question_column_list)
    csv_writer(answer_list, out_path_answer, answer_column_list)



# def worker(job_list):
#     for site in job_list:
#         file_processor(os.path.join(site,'Posts.xml'), '.\\output', site)
#         print('Finished processing '+site)

def worker(site):
    try:
        file_processor(os.path.join(site,'Posts.xml'), '.\\output', site)
        print('Finished processing '+site)
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    sites = os.listdir('.')
    sites.remove('output')
    p = mp.Pool(4)
    p.map(worker, sites)
    p.close()
    p.join()

