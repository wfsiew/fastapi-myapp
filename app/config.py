from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vesaliusServerCompanyCode: str = 'IHP'
    vesaliusServerSystemCode: str = 'MOBILE'
    vesaliusServerPassword: str = 'password'
    vesaliusServerBaseUrl: str = 'http://nh-uranus/ihp_uat/web_services/'
    
settings = Settings()