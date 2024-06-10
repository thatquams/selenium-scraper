from google.cloud import storage


def saveDataToCloud():

        # Create a Google Cloud Storage client
        client = storage.Client()       
        # Get the file to save
        file_path = '/carbin_webscraping/scrappedCars.json'

        # Create a bucket
        bucket = client.bucket('carbin-bucket')
        # Create a blob

        blob = bucket.blob('scrappedCars.json')
        # Open the file in binary mode

        with open(file_path, 'rb') as f:
            blob.upload_from_file(f)  