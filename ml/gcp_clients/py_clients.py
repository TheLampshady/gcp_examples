from google.cloud import storage, language, bigquery


class NLP(object):

    def __init__(self, project, bucket):
        self.bucket = bucket

        # Set up our GCS, NL, and BigQuery clients
        self.storage_client = storage.Client()
        self.nl_client = language.LanguageServiceClient()
        self.bq_client = bigquery.Client(project=project)
        self.table = self.get_table('article_data', 'news_classification_dataset')

    def set_data_set(self, data_set):
        data_set_ref = self.bq_client.dataset(data_set)
        self.data_set = bigquery.Dataset(data_set_ref)

    def get_table(self, table, data_set=None):
        if data_set:
            self.set_data_set(data_set)
        table_ref = self.data_set.table(table)
        return self.bq_client.get_table(table_ref)

    # Send article text to the NL API's classifyText method
    def classify_text(self, article):
        response = self.nl_client.classify_text(
            document=language.types.Document(
                content=article,
                type=language.enums.Document.Type.PLAIN_TEXT
            )
        )
        return response

    # Send files to the NL API and save the result to send to BigQuery
    def process_text(self):
        files = self.storage_client.bucket(self.bucket).list_blobs()
        print("Got article files from GCS, sending them to the NL API (this will take ~2 minutes)...")

        rows_for_bq = []

        for file in files:
            if file.name.endswith('txt'):
                article_text = file.download_as_string()
                nl_response = self.classify_text(article_text)
                if len(nl_response.categories) > 0:
                    rows_for_bq.append((article_text, nl_response.categories[0].name, nl_response.categories[0].confidence))

        print("Writing NL API article data to BigQuery...")
        # Write article text + category data to BQ
        errors = self.bq_client.insert_rows(self.table, rows_for_bq)
        assert errors == []


gcp_project = 'my-cgp-project'
gcp_bucket = 'my-bucket'
nlp = NLP(gcp_project, gcp_bucket)
nlp.process_text()
