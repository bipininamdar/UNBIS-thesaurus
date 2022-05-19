According to the UNBIS info page.

"The UNBIS Thesaurus is a multilingual database of the controlled vocabulary used to describe UN documents and other materials in the UN Library's collection.

The UNBIS Thesaurus grows as new topics are introduced to the agenda of the Organization and evolves as the language in the UN documents shifts over time. Controlled vocabulary makes subject searches possible by identifying documents on the same concept, even as terminology changes.

UNBIS Thesaurus concepts are used in the UN Digital Library and the Official Document System (ODS). In addition, other UN programmes, funds and regional commissions use the UNBIS Thesaurus for description of bibliographic materials and web content.

The UNBIS Thesaurus is available online in the six official UN languages, and for download in ttl, rdf/xml, csv or xlsx formats."

Thesaurus link: http://metadata.un.org/thesaurus/?lang=en 

The six languages are English, Russian, French, Arabic, Spanish, and Chinese (Mandarin, simplified characters).
The topics in the thesaurus are arranged in non-exclusive hierarchies and have lateral connections. So the structure is more like an ontology than a dictionary.
The JSON/xml/ttl file are only available for the "leaf" topics in the hierarchy. So info for "node" topics must be scraped from the web page.
There are 4 Python files for:

    Downloading the JSON files from the leaf topics
    Importing the JSON files and converting them into tables which will be later processed into CSV
    Scraping data for node topics
    Converting the tables into CSV files
