import json
import pandas
from os import path
import pickle
import os
import logging

data_location = "Z:\\DATA\\World Food Programme\\UNBIS\\compile jsons"
logfile = "Z:\\DATA\\World Food Programme\\UNBIS\\compile jsons\\log file.log"

# language_list = {'http://www.w3.org/2004/02/skos/core#altLabel',
#                      'http://www.w3.org/2004/02/skos/core#note',
#                      'http://www.w3.org/2004/02/skos/core#prefLabel',
#                      'http://www.w3.org/2004/02/skos/core#scopeNote'
#                      }

# relation_list = {'http://www.w3.org/2004/02/skos/core#related',
#                     'http://www.w3.org/2004/02/skos/core#broader',
#                     'http://www.w3.org/2004/02/skos/core#inScheme'
#                      }

# missed_fields = pandas.DataFrame({'file':[], 'larger field':[], 'missed sub field':[]})
# pickle.dump(missed_fields, open(path.join(data_location, "problem files\\missed_fields.p"), "wb"))

# problem_files = pandas.DataFrame({'filename':[], 'Description':[]})
# pickle.dump(problem_files, open(path.join(data_location, "problem files\\problem_files.p"), "wb"))

# def backup_pickle_files():
#     pickle.dump(shit_list, open(path.join(data_location, "json keys\\shit_list.p"), "wb"))
#     pickle.dump(watch_list, open(path.join(data_location, "json keys\\watch_list.p"), "wb"))
#     pickle.dump(relation_list, open(path.join(data_location, "json keys\\relation_list.p"), "wb"))
#     pickle.dump(language_list, open(path.join(data_location, "json keys\\language_list.p"), "wb"))
    # pickle.dump(problem_files, open(path.join(data_location, "problem files\\problem_files.p"), "wb"))
    # pickle.dump(core_altLabel, open(path.join(data_location, "data tables\\core#altLabel.p"), "wb"))
    # pickle.dump(core_prefLabel, open(path.join(data_location, "data tables\\core#prefLabel.p"), "wb"))
    # pickle.dump(core_related, open(path.join(data_location, "data tables\\core#related.p"), "wb"))
    # pickle.dump(core_broader, open(path.join(data_location, "data tables\\core#broader.p"), "wb"))
    # pickle.dump(core_inScheme, open(path.join(data_location, "data tables\\core#inScheme.p"), "wb"))
    # pickle.dump(core_note, open(path.join(data_location, "data tables\\core#note.p"), "wb"))
    # pickle.dump(core_scopeNote, open(path.join(data_location, "data tables\\core#scopeNote.p"), "wb"))

def add_to_list_of_languages(lang):
    list_of_languages = pickle.load(open(path.join(data_location, "json keys\list_of_languages.p"), "rb"))
    list_of_languages.update(lang)
    pickle.dump(list_of_languages, open(path.join(data_location, "json keys\list_of_languages.p"), "wb"))

def add_to_data_file(field, data, file):
    try:
        historic_data = pickle.load(open(path.join(data_location, "data tables\\"+ field + ".p"), "rb"))
    except FileNotFoundError as exc:
        logging.basicConfig(filename=logfile, level=logging.WARNING, format='%(message)s')
        logging.warning("creating file" + "\t" + field + ".p")
        pickle.dump(data, open(path.join(data_location, "data tables\\"+ field + ".p"), "wb"))
        return

    try:
        historic_data = historic_data.append(data, ignore_index=True)
        pickle.dump(historic_data, open(path.join(data_location, "data tables\\" + field + ".p"), "wb"))
    except Exception as exc:
        logging.basicConfig(filename=logfile, level=logging.WARNING, format='%(message)s')
        logging.warning("some problem in writing data to file" + "\t" + field + "\t" + str(file) + "\t" + exc)

def cleanse_link(link:str):
    return link.split('/')[-1]

if __name__ == "__main__":

    watch_list = pickle.load(open(path.join(data_location, "json keys\\watch_list.p"), "rb"))
    shit_list = pickle.load(open(path.join(data_location, "json keys\\shit_list.p"), "rb"))
    relation_list = pickle.load(open(path.join(data_location, "json keys\\relation_list.p"), "rb"))
    language_list = pickle.load(open(path.join(data_location, "json keys\\language_list.p"), "rb"))
    problem_files = pickle.load(open(path.join(data_location, "problem files\\problem_files.p"), "rb"))
    missed_fields = pickle.load(open(path.join(data_location, "problem files\\missed_fields.p"), "rb"))

    for files in os.listdir("Z:\\DATA\\World Food Programme\\UNBIS\\jsondata"):
        with open(os.path.join("Z:\\DATA\\World Food Programme\\UNBIS\\jsondata", files), encoding="UTF-8") as file:

            logging.basicConfig(filename=logfile, level=logging.WARNING, format='%(message)s')
            logging.warning("processing file" + "\t" + file.name)

            data = json.load(file)[0]

            try:
                id = cleanse_link(data['@id'])
            except Exception as exc:
                problem_files = problem_files.append(({'filename': file.name, 'Description': '@id field not found'}))
                pickle.dump(problem_files, open(path.join(data_location, "problem files\\problem_files.p"), "wb"))
                continue
            try:
                entity_type = data['@type']
            except Exception as exc:
                problem_files = problem_files.append(({'filename': file.name, 'Description': '@type field not found'}))
                pickle.dump(problem_files, open(path.join(data_location, "problem files\\problem_files.p"), "wb"))

            for field in data:
                if field in shit_list:
                    continue

                elif field in language_list:
                    try:
                        table = pandas.json_normalize(data[field])

                        for t in table:
                            if t != '@language' and t != '@value':
                                missed_fields = missed_fields.append({'file': file, 'larger field': field, 'missed sub field': t})
                                pickle.dump(missed_fields, open(path.join(data_location, "problem files\\missed_fields.p"), "wb"))

                        table2 = table.groupby('@language', as_index=False)['@value'].apply('|'.join)

                        # Uncomment before execution
                        add_to_list_of_languages(tuple(table2['@language']))

                    except Exception as exc:
                        logging.basicConfig(filename=logfile, level=logging.WARNING, format='%(message)s')
                        logging.warning("Error in language field" + "\t" + field + "\t" + file.name)
                        problem_files = problem_files.append({'filename': file.name, 'Description': field})
                        pickle.dump(problem_files, open(path.join(data_location, "problem files\\problem_files.p"), "wb"))

                    table2['id'] = id
                    add_to_data_file(field.split('/')[-1], table2, id)

                elif field in relation_list:
                    table = pandas.json_normalize(data[field])

                    for t in table:
                        if t != '@id':
                            missed_fields = missed_fields.append({'file': file, 'larger field': field, 'missed sub field': t})
                            pickle.dump(missed_fields,open(path.join(data_location, "problem files\\missed_fields.p"), "wb"))

                    value_concat = []
                    for value in (table['@id'].values):
                        value_concat.append(cleanse_link(value))

                    table['relation'] = value_concat
                    table['id'] = id
                    table = table.drop(columns='@id')
                    table2 = table.groupby('id', as_index=False)['relation'].apply('|'.join)
                    add_to_data_file(field.split('/')[-1], table2, id)

                else:
                    watch_list.update([str(file), field])
                    pickle.dump(watch_list, open(path.join(data_location, "json keys\\watch_list.p"), "wb"))