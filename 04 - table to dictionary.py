import pickle
import os
import pandas
import csv

data_location = "Z:\\DATA\\World Food Programme\\UNBIS"

if __name__ == "__main__":
    for files in os.listdir("Z:\\DATA\\World Food Programme\\UNBIS\\compile jsons\\data tables"):

        locals()[files.split(".")[0]] = pickle.load(open(os.path.join(data_location, "compile jsons\\data tables\\"+files), "rb"))

    description = locals()['core#scopeNote'].append(locals()['core#note'])
    description_final = description.groupby(['id', '@language'], as_index=False)['@value'].apply('\n'.join)

    synonyms = locals()['core#prefLabel'].append(locals()['core#altLabel'])
    synonyms_final = synonyms.groupby(['id', '@language'], as_index=False)['@value'].apply('|'.join)

    description_final  = pandas.merge(description_final, synonyms_final, how = 'outer',  on = ["id", "@language"])

    description_final = description_final.rename(columns={'@value_x': 'Description', '@value_y':'Synonyms'})

    final = pandas.merge(description_final, locals()['core#prefLabel'], how='outer', on=["id", "@language"])
    final = final.rename(columns={'@value': 'Preferred Label'})

    final = pandas.merge(final, locals()['core#related'],  how = 'outer',  on = ["id"])
    final = final.rename(columns={'relation':'SimilarTo'})

    final = pandas.merge(final, locals()['core#inScheme'], how='outer', on=["id"])
    final = final.rename(columns={'relation': 'is_instance'})

    final['has_instance'] = ""
    final['POS'] = "Noun"

    final = pandas.merge(final, locals()['core#broader'], how='outer', on=["id"])
    final = final.rename(columns={'relation': 'Hypernym'})

    final = final.append(locals()['links_without_JSON_descriptions'], ignore_index=True)

    final = final.rename(columns={'id': 'Class ID'})

    for language in locals()['list_of_languages']:

        language_final = final.loc[final['@language'] == language]

        link_column = []

        for x in language_final.index:
            link_column.append(str("http://metadata.un.org/thesaurus/"+str(language_final.loc[x]['Class ID'])+"?lang="+str(language)))
        language_final = language_final.assign(Link= link_column)
        language_final = language_final.drop(columns='@language')
        language_final.to_csv(os.path.join(data_location, 'dict file_'+language+'.csv'), index = False, quoting = csv.QUOTE_NONNUMERIC)