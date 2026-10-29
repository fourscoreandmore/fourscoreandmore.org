import os

appRoot = os.environ.get('PLATFORM_APP_DIR') or os.path.dirname(
    os.path.dirname(__file__))


class Config(object):
    PREFIX = os.environ.get('APP_PATH') or '/apps'
    SECRET_KEY = os.environ.get(
        'PLATFORM_PROJECT_ENTROPY') or 'development_secret_key'
    SCORE_PATH = os.path.join(appRoot, "resources/scores")
    SCORE_DOWNLOAD_URI_PREFIX = "/apps/download/"
    SCORE_DOWNLOAD_PATH = appRoot + "/download/scores"
    LIEDER_CORPUS_PATH = os.path.join(appRoot, "When-in-Rome/Corpus/OpenScore-LiederCorpus")
    LIEDER_INDEX_PATH = os.path.join(appRoot, "resources/scores/lieder.jsonl")
    CORPUS_DOWNLOAD_PATH = os.path.join(appRoot, "When-in-Rome/Corpus/OpenScore-LiederCorpus")
    WIH_WRITABLE_PATH = os.path.join(appRoot, "wih-writable")
    # Working in Harmony score uploads; other forms post far less.
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # The most an uploaded .mxl may unzip to.
    WIH_MAX_UNZIPPED_SIZE = 50 * 1024 * 1024
    # Seconds a Working in Harmony analysis may take before it's stopped.
    WIH_TIME_LIMIT = 60
