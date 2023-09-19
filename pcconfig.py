import pynecone as pc

class KakaoDeveloperesHelperBotConfig(pc.Config):
    pass

config = KakaoDeveloperesHelperBotConfig(
    app_name="kakao-developers-helper-bot",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)