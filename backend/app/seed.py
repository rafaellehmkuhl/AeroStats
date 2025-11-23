from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import User, Team, ClassType, TeamBatteryStatus, SystemState
from app.core.security import get_password_hash

def seed():
    create_db_and_tables()
    with Session(engine) as session:
        # Create Admin
        admin_email = "admin@aerostats.com"
        if not session.exec(select(User).where(User.email == admin_email)).first():
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                role="admin"
            )
            session.add(admin)
            print("Admin created")

        # Create Regular Teams
        if not session.exec(select(Team).where(Team.class_ == "regular")).first():
            teams = [
                Team(year_id=1, name="Axé Fly", country="Brazil", state="BA", university="Universidade Federal da Bahia (UFBA)", class_="regular"),
                Team(year_id=2, name="EESC-USP Alpha", country="Brazil", state="SP", university="Escola de Engenharia de São Carlos - Universidade de São Paulo (EESC - USP)", class_="regular"),
                Team(year_id=3, name="F-Carranca", country="Brazil", state="BA", university="Universidade Federal do Vale do São Francisco (UNIVASF)", class_="regular"),
                Team(year_id=4, name="Harpia AeroDesign", country="Brazil", state="SP", university="Universidade Federal do ABC (UFABC)", class_="regular"),
                Team(year_id=5, name="AeroFEG", country="Brazil", state="SP", university='Universidade Estadual Paulista "Júlio de Mesquita Filho" (UNESP) - Campus', class_="regular"),
                Team(year_id=6, name="FEI Regular", country="Brazil", state="SP", university="Centro Universitário da FEI (FEI)", class_="regular"),
                Team(year_id=7, name="Falcons AeroDesign", country="Brazil", state="SP", university="Centro Universitário FACENS (FACENS)", class_="regular"),
                Team(year_id=8, name="Uai, sô! Fly!!! AeroDesign", country="Brazil", state="MG", university="Universidade Federal de Minas Gerais (UFMG)", class_="regular"),
                Team(year_id=9, name="Keep Flying", country="Brazil", state="SP", university="Universidade de São Paulo - Escola Politécnica (Poli-USP)", class_="regular"),
                Team(year_id=10, name="Urubus AeroDesign", country="Brazil", state="SP", university="Faculdade de Engenharia de Guarulhos / Faculdade associada (curso de Engenharia)", class_="regular"),
                Team(year_id=11, name="Acalântis", country="Brazil", state="PR", university="Universidade Federal do Paraná (UFPR) - Campus", class_="regular"),
                Team(year_id=12, name="CEFAST AeroDesign", country="Brazil", state="MG", university="Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG) - Campus", class_="regular"),
                Team(year_id=13, name="Albatroz AeroDesign", country="Brazil", state="SC", university="Universidade do Estado de Santa Catarina (UDESC)", class_="regular"),
                Team(year_id=14, name="Tucano", country="Brazil", state="MG", university="Universidade Federal de Uberlândia (UFU)", class_="regular"),
                Team(year_id=16, name="UTFalcon AeroDesign", country="Brazil", state="PR", university="Universidade Federal do Paraná (UFPR) - Campus Ponta Grossa", class_="regular"),
                Team(year_id=18, name="Montenegro", country="Brazil", state="SP", university="Instituto Tecnológico de Aeronáutica (ITA) / Faculdade ligada à aviação", class_="regular"),
                Team(year_id=19, name="Nisus AeroDesign", country="Brazil", state="SC", university="Universidade Federal de Santa Catarina (UFSC) - Campus Joinville", class_="regular"),
                Team(year_id=20, name="Megazord AeroDesign", country="Brazil", state="SP", university='Universidade de São José dos Campos "Prof. Jesse" (nome institucional completo)', class_="regular"),
                Team(year_id=21, name="BlackBird AeroDesign", country="Brazil", state="RJ", university="Universidade Federal Fluminense (UFF) - Campus Niterói", class_="regular"),
                Team(year_id=22, name="Zeus", country="Brazil", state="MA", university="Universidade Estadual do Maranhão (UEMA)", class_="regular"),
                Team(year_id=23, name="Kukulcán AeroDesign", country="Mexico", state="MX", university="Instituto Tecnológico Superior de Ingeniería Mecánica", class_="regular"),
                Team(year_id=24, name="Falcão Branco Aerodesign", country="Brazil", state="SP", university="Faculdade Hermínio Ometto (FHO) - UNIARARAS/UNI", class_="regular"),
                Team(year_id=25, name="PegAzuls AeroDesign", country="Brazil", state="RN", university="Universidade Federal do Semi-Árido (UFERSA) - Campus Mossoró", class_="regular"),
                Team(year_id=26, name="AeroScorpion", country="Brazil", state="SP", university="Instituto Federal de São Paulo (IFSP) - Campus Araraquara", class_="regular"),
                Team(year_id=27, name="Triângulo Aéreo AeroDesign", country="Brazil", state="MG", university="Universidade Federal do Triângulo Mineiro (UFTM)", class_="regular"),
                Team(year_id=28, name="Zebra", country="Brazil", state="SP", university='Universidade Estadual "Júlio de Mesquita Filho" - Campus (UNESP) / Faculdade', class_="regular"),
                Team(year_id=29, name="Abutres AeroDesign", country="Brazil", state="PR", university="Universidade Estadual do Paraná - Campus Cornélio Procópio (UEPG/UNESPAR)", class_="regular"),
                Team(year_id=30, name="Minerva AeroDesign", country="Brazil", state="RJ", university="Universidade Federal do Rio de Janeiro - Campus (UFRJ) / Faculdade de Engenharia", class_="regular"),
                Team(year_id=31, name="Dragão Branco AeroDesign", country="Brazil", state="SP", university="Universidade Federal de São Carlos (UFSCar)", class_="regular"),
                Team(year_id=32, name="Skywards UFVoa", country="Brazil", state="MG", university="Universidade Federal de Viçosa (UFV) - Campus Viçosa", class_="regular"),
                Team(year_id=33, name="Draco Volans", country="Brazil", state="DF", university="Universidade de Brasília (UnB) - Campus", class_="regular"),
                Team(year_id=34, name="Burning Goose", country="Brazil", state="PR", university="Universidade Federal do Paraná (UFPR)", class_="regular"),
                Team(year_id=35, name="Uirá AeroDesign", country="Brazil", state="MG", university="Universidade Federal de Itajubá (UNIFEI) - Campus Itajubá", class_="regular"),
                Team(year_id=36, name="ADAM AeroDesign", country="Brazil", state="PR", university="Universidade Estadual de Maringá (UEM)", class_="regular"),
                Team(year_id=37, name="Araras AeroDesign", country="Brazil", state="SE", university="Universidade Federal de Sergipe (UFS)", class_="regular"),
                Team(year_id=38, name="Delta do Piauí AeroDesign", country="Brazil", state="PI", university="Universidade Federal do Piauí (UFPI)", class_="regular"),
                Team(year_id=39, name="Aerocária PUCPR", country="Brazil", state="PR", university="Pontifícia Universidade Católica do Paraná (PUCPR)", class_="regular"),
                Team(year_id=40, name="AeroJampa", country="Brazil", state="PB", university="Universidade Federal da Paraíba (UFPB)", class_="regular"),
                Team(year_id=41, name="Pampa AeroDesign", country="Brazil", state="RS", university="Universidade Federal do Rio Grande do Sul (UFRGS)", class_="regular"),
                Team(year_id=42, name="Grifo AeroDesign", country="Brazil", state="PR", university="Universidade Federal do Paraná (UFPR) - Campus Londrina", class_="regular"),
                Team(year_id=43, name="AeroDuca", country="Brazil", state="SP", university="Centro Universitário Anhembi Morumbi (Anhembi Morumbi)", class_="regular"),
                Team(year_id=45, name="Enterprise", country="Brazil", state="SP", university="Universidade do Vale do Paraíba (UNIVAP)", class_="regular"),
                Team(year_id=46, name="Aerocócus UPF", country="Brazil", state="RS", university="Universidade de Passo Fundo (UPF)", class_="regular"),
                Team(year_id=47, name="Loadmaster Regular", country="Brazil", state="MG", university="Pontifícia Universidade Católica de Minas Gerais (PUC Minas)", class_="regular"),
                Team(year_id=48, name="AeroBeetle", country="Brazil", state="MA", university="Universidade Estadual do Maranhão (UEMA) - Campus São Luís (Pitágoras)", class_="regular"),
                Team(year_id=49, name="Ozires USJT AeroDesign", country="Brazil", state="SP", university="Universidade São Judas Tadeu (USJT)", class_="regular"),
                Team(year_id=50, name="MasBáh", country="Brazil", state="RS", university="Faculdade Horizontina (FAHOR)", class_="regular"),
                Team(year_id=51, name="Caboclo AeroDesign", country="Brazil", state="PE", university="Universidade Federal de Pernambuco (UFPE) - Unidade Acadêmica", class_="regular"),
                Team(year_id=52, name="Aracuã AeroDesign", country="Brazil", state="MS", university="Universidade Federal da Grande Dourados (UFGD)", class_="regular"),
                Team(year_id=53, name="Aerodactyl", country="Brazil", state="GO", university="Universidade Federal de Goiás (UFG)", class_="regular"),
                Team(year_id=54, name="EPAER AeroDesign", country="Brazil", state="PR", university="Universidade Federal do Paraná (UFPR) - Campus Pato Branco", class_="regular"),
                Team(year_id=55, name="Eniac SkyForce", country="Brazil", state="SP", university="Centro Universitário Eniac (ENIAC)", class_="regular"),
                Team(year_id=56, name="Aratinga AeroDesign", country="Brazil", state="CE", university="Universidade Federal do Ceará (UFC) - Campus Russas", class_="regular"),
                Team(year_id=57, name="pe Accipiter Tecnologia e AeroDee", country="Brazil", state="SP", university="Centro de Tecnologia de São Paulo (nome institucional)", class_="regular"),
                Team(year_id=58, name="IFly AeroDesign", country="Brazil", state="MG", university="Universidade do Sudeste de Minas Gerais (UNIFEM / nome institucional)", class_="regular"),
                Team(year_id=59, name="U-Fly AeroDesign", country="Mexico", state="MX", university="Universidad Aeronáutica en Querétaro (UNAQ)", class_="regular"),
            ]
            for t in teams:
                session.add(t)
            print("Regular Teams created")

        # Create Micro Teams
        if not session.exec(select(Team).where(Team.class_ == "micro")).first():
            micro_teams = [
                Team(year_id=202, name="Trem Ki Voa Micro", country="Brazil", state="MG", university="Universidade Federal de São João del-Rei - Campus Santo Antônio (UFSJ - Santo Antônio)", class_="micro"),
                Team(year_id=215, name="Uai, sô! Fly!!! AeroDesign Micro", country="Brazil", state="MG", university="Universidade Federal de Minas Gerais (UFMG)", class_="micro"),
                Team(year_id=223, name="Tucano Micro", country="Brazil", state="MG", university="Universidade Federal de Uberlândia (UFU)", class_="micro"),
                Team(year_id=211, name="Uirá Micro", country="Brazil", state="MG", university="Universidade Federal de Itajubá - Campus Itajubá (UNIFEI - Itajubá)", class_="micro"),
                Team(year_id=203, name="Carancho Micro", country="Brazil", state="RS", university="Universidade Federal de Santa Maria (UFSM)", class_="micro"),
                Team(year_id=204, name="MicroRaptor", country="Brazil", state="MG", university="Universidade Federal de Juiz de Fora (UFJF)", class_="micro"),
                Team(year_id=206, name="Mamutes de Cerrado AeroDesign", country="Brazil", state="DF", university="Universidade de Brasília - Campus Faculdade do Gama (FGA - UnB)", class_="micro"),
                Team(year_id=201, name="EESC-USP Bravo", country="Brazil", state="SP", university="Universidade de São Paulo - Escola de Engenharia de São Carlos (EESC - USP)", class_="micro"),
                Team(year_id=216, name="Adelphi Rookie AeroDesign Team", country="Brazil", state="SP", university='Universidade Estadual Paulista "Júlio de Mesquita Filho" - Campus São João da Boa Vista (UNESP-SJBV)', class_="micro"),
                Team(year_id=207, name="Taperá Baby", country="Brazil", state="SP", university="Instituto Federal de Educação, Ciência e Tecnologia de São Paulo - Campus Salto (IFSP - Salto)", class_="micro"),
                Team(year_id=212, name="Céu Azul Aeronaves", country="Brazil", state="SC", university="Universidade Federal de Santa Catarina - Campus Florianópolis (UFSC - Florianópolis)", class_="micro"),
                Team(year_id=213, name="Keep Flying Jr.", country="Brazil", state="SP", university="Universidade de São Paulo - Escola Politécnica (Poli - USP)", class_="micro"),
                Team(year_id=205, name="Albatroz AeroDesign Micro", country="Brazil", state="SC", university="Universidade do Estado de Santa Catarina (UDESC)", class_="micro"),
                Team(year_id=208, name="Acauã Micro", country="Brazil", state="MG", university="Universidade Federal de Viçosa - Campus Florestal (UFV - Florestal)", class_="micro"),
                Team(year_id=209, name="L.O.T.S. AeroDesign Micro", country="Brazil", state="MG", university="Universidade Federal de Itajubá - Campus Itabira (UNIFEI - Itabira)", class_="micro"),
                Team(year_id=217, name="Mandacaru AeroDesign Micro", country="Brazil", state="PE", university="Universidade Federal de Pernambuco (UFPE)", class_="micro"),
                Team(year_id=218, name="Tenpest AeroDesign", country="Brazil", state="PE", university="Universidade de Pernambuco (UPE)", class_="micro"),
                Team(year_id=222, name="AeroCataratas Micro", country="Brazil", state="PR", university="Universidade Estadual do Oeste do Paraná (UNIOESTE)", class_="micro"),
                Team(year_id=219, name="Loadmaster Micro", country="Brazil", state="MG", university="Pontifícia Universidade Católica de Minas Gerais (PUC Minas)", class_="micro"),
                Team(year_id=220, name="UFForce AeroDesign Micro", country="Brazil", state="RJ", university="Universidade Federal Fluminense - Campus Volta Redonda (UFF - Volta Redonda)", class_="micro"),
            ]
            for t in micro_teams:
                session.add(t)
            print("Micro Teams created")

        # Create Advanced Teams
        if not session.exec(select(Team).where(Team.class_ == "advanced")).first():
            advanced_teams = [
                Team(year_id=101, name="Adelphi AeroDesign", country="Brazil", state="SP", university="Universidade Estadual Paulista (UNESP) / Campus", class_="advanced"),
                Team(year_id=108, name="EESC-USP Charlie", country="Brazil", state="SP", university="Escola de Engenharia de São Carlos - Universidade de São Paulo (EESC - USP)", class_="advanced"),
                Team(year_id=102, name="Urutau AeroDesign", country="Brazil", state="AM", university="Universidade Federal do Amazonas (UFAM)", class_="advanced"),
                Team(year_id=103, name="Canarinho AeroDesign", country="Brazil", state="SP", university="Universidade de São Paulo (USP)", class_="advanced"),
                Team(year_id=107, name="Aero Chico", country="Brazil", state="BA", university="Universidade Federal da Bahia (UFBA)", class_="advanced"),
                Team(year_id=104, name="Car-Kará Advanced", country="Brazil", state="RN", university="Universidade Federal do Rio Grande do Norte (UFRN)", class_="advanced"),
                Team(year_id=106, name="Venturi AeroDesign", country="Brazil", state="RJ", university="Centro Federal de Educação Tecnológica Celso Suckow da Fonseca (CEFET-RJ)", class_="advanced"),
                Team(year_id=110, name="LoadMaster Advanced", country="Brazil", state="MG", university="Pontifícia Universidade Católica de Minas Gerais (PUC Minas)", class_="advanced"),
                Team(year_id=105, name="Findus", country="Sweden", state="SE", university="Linköping University (Linköping Univ.)", class_="advanced"),
                Team(year_id=109, name="Raptor Advanced", country="Brazil", state="MG", university="Universidade Federal de Minas Gerais (UFMG)", class_="advanced"),
            ]
            for t in advanced_teams:
                session.add(t)
            print("Advanced Teams created")

        # Initialize SystemState
        if not session.get(SystemState, 1):
            session.add(SystemState(id=1))
            print("SystemState initialized")

        session.commit()

if __name__ == "__main__":
    seed()
