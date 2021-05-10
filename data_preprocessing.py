import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import logging

logger = logging.getLogger(__name__)


class NewsDetection:
    df = pd.read_csv(r"news.csv")

    @staticmethod
    def data_processing():
        df = NewsDetection.df
        labels = NewsDetection.df.label
        x_train, x_test, y_train, y_test = train_test_split(df['text'], labels, test_size=0.2, random_state=7)

        # Initialize a TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        # DataFlair - Fit and transform train set, transform test set
        tfidf_train = tfidf_vectorizer.fit_transform(x_train)
        tfidf_test = tfidf_vectorizer.transform(x_test)

        # Initialize a PassiveAggressiveClassifier
        pac = PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train, y_train)
        # Predict on the test set and calculate accuracy
        y_predict = pac.predict(tfidf_test)
        score = accuracy_score(y_test, y_predict)
        logger.info('Accuracy: {}'.format(round(score * 100, 2)))
        return y_test, y_predict


if __name__ == "__main__":
    result_test, result_pred = NewsDetection.data_processing()
    logger.info("result:{}/{}".format(result_test, result_pred))
    matrix = confusion_matrix(result_test, result_pred, labels=['FAKE', 'REAL'])
    print(matrix)
