# 크롤링
import requests
from bs4 import BeautifulSoup

# Langchain 패키지들
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

# 구글 번역 API
from deep_translator import GoogleTranslator

class SearchService:

    @staticmethod
    def get_recipe(ramen_name):
        client_naver_id = "IKcG8rBOOcr_3Uw1FpgS"
        client_naver_secret = "wN4qgCQjJa"

        # naver api URL 설정
        url = f"https://openapi.naver.com/v1/search/blog?query={ramen_name}&display=10&sort=sim"

        # 헤더 설정
        headers = {
            "X-Naver-Client-Id": client_naver_id,
            "X-Naver-Client-Secret": client_naver_secret,
        }

        # API 호출
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            data = res.json()

            # 관련 글 링크
            links = [data["items"][i]["link"] for i in range(min(5, len(data["items"])))]

            # 블로그 글 가져오기 
            contents = [SearchService.fetch_post_content(link) for link in links]
            return contents, links
        else:
            return [f"Error {res.status_code}: {res.text}"], []

    @staticmethod
    def fetch_post_content(link):
        try:
            res_recipe = requests.get(link)
            pars_recipe = BeautifulSoup(res_recipe.content, "html.parser")
            iframe = pars_recipe.find("iframe", id="mainFrame")
            if not iframe:
                return "Iframe이 없습니다."
            
            iframe_src = iframe["src"]
            iframe_url = f"https://blog.naver.com{iframe_src}"
            res_iframe = requests.get(iframe_url)
            soup_iframe = BeautifulSoup(res_iframe.content, "html.parser")
            post_content = soup_iframe.find("div", class_="se-main-container")
            if post_content:
                return post_content.get_text(separator="\n", strip=True)
            else:
                return "블로그 글이 없습니다."
        except Exception as e:
            return f"블로그 글 로드 오류. {link}: {str(e)}"

    @staticmethod
    def gpt_ramen(ramen_name, blog_contents):
        api_key = "sk-proj-0cVfxjh0glwRGoOTQ2NXT3BlbkFJslAa7FuWt8YGPA408NVc"
        # 자연어-> 벡터(임베딩 작업, 유사도로 이해할 수 있게 벡터로 변환하는 작업)
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        # 주어진 자료
        knowledge_base = FAISS.from_texts(blog_contents, embeddings)
        # 주어진 자료에서 유저의 질문과 유사도 파악
        docs = knowledge_base.similarity_search(ramen_name)

        # 모델 설정
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=api_key,
            max_tokens=2000,
            model_name="gpt-4o",
            request_timeout=120,
        )
        chain = load_qa_chain(llm, chain_type="stuff")
        # 결과 값
        gpt_response = chain.invoke({"input_documents": docs, "question": ramen_name})
        output_text = gpt_response.get("output_text", "")
        gpt_ramen_recipe = SearchService.google_trans(output_text)
        return gpt_ramen_recipe

    @staticmethod
    def google_trans(message):
        translator = GoogleTranslator(source="auto", target="ko")
        if isinstance(message, dict):
            message = message.get("output_text", "")
        if not isinstance(message, str):
            return "적절한 글이 아닙니다."
        try:
            trans_result = translator.translate(message)
        except Exception as e:
            trans_result = f"번역 오류: {str(e)}"
        return trans_result