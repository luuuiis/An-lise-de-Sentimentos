from selenium import webdriver
from bs4 import BeautifulSoup
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time

# Configurar o ChromeDriver (certifique-se de substituir 'caminho_para_o_chromedriver' pelo caminho correto)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()
driver.get("https://google.com")

# URL do produto na Amazon que você deseja analisar
url = r"https://www.amazon.com.br/Echo-Dot-5%C2%AA-gera%C3%A7%C3%A3o-Cor-Preta/dp/B09B8VGCR8/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2EO0I2221E3VL&keywords=alexa&qid=1699731403&s=electronics&sprefix=alexa%2Celectronics%2C215&sr=1-1&ufe=app_do%3Aamzn1.fos.95de73c3-5dda-43a7-bd1f-63af03b14751&th=1"

# Abra a página do produto no navegador virtual
driver.get(url)

# Exemplo: Role a página algumas vezes para carregar mais comentários
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Espere um pouco para o novo conteúdo ser carregado
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Aguarde um tempo para garantir que a página seja totalmente carregada
import time
time.sleep(5)

# Obtenha o HTML da página
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

comentarios = soup.find_all('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content')
textos_comentarios = [comentario.text for comentario in comentarios]
sia = SentimentIntensityAnalyzer()

# Realize a análise de sentimentos para cada comentário
for comentario in textos_comentarios:
    sentiment = sia.polarity_scores(comentario)
    print(f"Comentário: {comentario}")
    print(f"Sentimento: {sentiment}")

