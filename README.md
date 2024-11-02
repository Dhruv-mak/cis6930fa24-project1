# Redaction Program

This program redacts sensitive information from text files such as names, dates, phone numbers, addresses, and concepts. It uses the spaCy NLP library to process and redact the text.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
  - [Date Redactor](#date-redactor)
  - [Phone Redactor](#phone-redactor)
  - [Name Redactor](#name-redactor)
  - [Address Redactor](#address-redactor)
  - [Concept Redactor](#concept-redactor)
- [Pipeline](#pipeline)
- [Demo Video](#demo-video)
- [Bugs](#bugs)
- [Assumptions](#assumptions)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Dhruv-mak/cis6930fa24-project1.git
   cd cis6930fa24-project1
   ```

2. Install the required packages:
   ```bash
   pipenv install -e .
   ```

3. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_trf
   ```

## Usage

Run the redaction program using the following command:

```bash
pipenv run python redactor.py --input "data/*.txt" --output "redacted_output" [OPTIONS]
```
To run the python test cases

```bash
pipenv run python -m pytest
```

### Options

- `--names`: Redact names
- `--dates`: Redact dates
- `--phones`: Redact phone numbers
- `--addresses`: Redact addresses
- `--concept "concept_name"`: Redact specified concepts (can be multiple)
- `--stats`: Output file for stats

## Components

### Date Redactor

The date redactor identifies date entities in a document using regex patterns from the `commonregex` library and named entity recognition (NER) from spaCy. It uses the `DATE_REGEX` pattern from the `commonregex` library to find date patterns in the text. It additionally checks tokens with the entity type `DATE` as recognized by spaCy’s named entity recognition. For tokens that match the regex pattern or have the entity type `DATE`, it sets the custom attribute `token._.redact` to `True`. The identified redactions are logged using the `log_redactions` function for monitoring and auditing purposes.

### Phone Redactor

The phone redactor identifies phone number entities in a document using regex patterns from the `commonregex` library. It uses the `PHONE_REGEX` pattern from the `commonregex` library to find phone number patterns in the text. For tokens that match the regex pattern, it sets the custom attribute `token._.redact` to `True`. The identified redactions are logged using the `log_redactions` function for monitoring and auditing purposes.

### Name Redactor

The name redactor identifies names in a document using a combination of email extraction and named entity recognition (NER) from spaCy. It uses the `EMAIL_REGEX` pattern from the `commonregex` library to find email patterns in the text and extracts potential names from email usernames. These names are validated using the `names_dataset` library. Additionally, it checks tokens with the entity type `PERSON` as recognized by spaCy’s NER. For tokens that match the extracted names or have the entity type `PERSON`, it sets the custom attribute `token._.redact` to `True`. The identified redactions are logged using the `log_redactions` function for monitoring and auditing purposes.

### Address Redactor

The address redactor identifies addresses in a document using `pyap` and marks them for redaction. It extracts addresses using `pyap.parse` and locates their start and end positions in the text. Additionally, it checks tokens with the named entity types `GPE` (Geopolitical Entity), `LOC` (Location), and `FAC` (Facility) as recognized by spaCy’s Named Entity Recognition (NER). If an address is found or a token matches one of the specified entity types, all relevant tokens are marked for redaction by setting the custom attribute `token._.redact` to `True`. The identified redactions are logged using the `log_redactions` function for monitoring and auditing purposes.


### Concept Redactor

The concept redactor identifies and marks sentences related to specific concepts in a document for redaction. It uses the Datamuse API to find related words and utilizes the Hugging Face zero-shot classification model (`facebook/bart-large-mnli`) to accurately determine sentence relevance. If a sentence is found to be related to the specified concepts or their related words, all tokens in that sentence are marked for redaction by setting the custom attribute `token._.redact` to `True`. The identified redactions are logged using the `log_redactions` function for monitoring and auditing purposes.


## Pipeline

1. **Custom Tokenizer**: A custom tokenizer is defined to handle special characters.
2. **Redaction Components**: Different components are added to the spaCy pipeline to handle specific types of entities such as names, dates, phone numbers, addresses, and concepts.
3. **Processing Files**: Each input file is processed by the pipeline, and the identified entities are redacted.
4. **Logging**: The redaction process and stats are logged accordingly, and the redacted content is saved to the output directory.

## Demo Video

![Running test](https://github.com/user-attachments/assets/87c4b936-b87c-4d89-a238-957720b97206)

## Bugs

- **Caveat with Named Entities**: The redactors use regex patterns and may not catch all variations or formats of the entities they are designed to identify.
- **Custom Tokenizer Issues**: Sometimes the custom tokenizer might not correctly tokenize sentences with unusual delimiters, which may lead to incomplete redaction.
- **Address Redactor Limitation**: The address parser uses `pyap`, which works only for properly formatted addresses. Addresses that do not conform to expected formats may not be redacted.
- **Name Redactor Limitation**: For name redactor to work properly the name should be present in any email or the context of the sentence should suggest that part is name.
- **Concept Redactor Flakiness**: The concept redactor generally works well but can occasionally miss obvious concepts, leading to incomplete redaction. This may be due to limitations in the similarity measures or zero-shot classification model inaccuracies.

## Assumptions

- The input files are plain text files.
- Dates, names, phone numbers, and addresses follow standard formats that can be identified using regex patterns.
- The concepts to be redacted are clearly defined and their related words can be found using WordNet.
- The input folder glob has text files.

## Author

- [Dhruv Makwana](https://github.com/Dhruv-mak)