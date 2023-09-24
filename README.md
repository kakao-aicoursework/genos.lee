# genos.lee
genos.lee의 저장소입니다.

## Requirement
- 실행 전에 아래와 같이 api key를 환경변수로 export 해야 합니다.
```
export OPENAI_API_KEY={api-key}
```

## 실행 방법
- 주의사항: pynecone과 chroma-api를 다른 virtualenv환경에서 실행해주세요. 

### pynecone 
- 터미널에서 아래 명령어를 실행해주세요. 
```shell
virtualenv venv
pip install -r requirements.txt
pc init
pc run
```

### chroma api 실행 방법
- 터미널에서 아래 명령어를 실행해주세요. 
```shell
cd chroma_api
virtualenv api-env
pip install -r requirements.txt
uvicorn chroma_api:api --reload --port 9000
```