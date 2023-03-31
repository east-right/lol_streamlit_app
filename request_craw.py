import requests
from urllib import parse
import json

class craw:
    def __init__(self):
        with open('pre_label.json', 'r') as f: #ver2 에선 pre_label.json
            self.dic = json.load(f)
    def craw_data(self,name):
        enb = parse.quote(name)#유저 닉네임 유니코드화
        
        path = f'https://api.your.gg/kr/api/profile/{enb}?lang=ko'#전적갱신시 가져오는 데이터 URL
        main = requests.post(path).json()#데이터 requests로 받아오고 json화
        try:
            target = main['soloRankTier']+ ' '+ self.dic['rank_num'][main['soloRankRank']]#현재티어
            num_game = main['soloRankWins'] + main['soloRankLoses']#이번시즌 플레이판수
            
            
            path2 = f'https://api.your.gg/kr/api/profile/{enb}?lang=ko&matchCategory=&listMatchCategory='#유저 데이터
            sub = requests.get(path2).json()
            
            #저번시즌 티어
            try:
                if len(sub['soloRankHistory']) == 2:
                    before_season = sub['soloRankHistory'][1]['tier'] + ' ' + sub['soloRankHistory'][1]['division']
                else:
                    before_season = sub['soloRankHistory'][0]['tier'] + ' ' + sub['soloRankHistory'][0]['division']
            except:
                before_season = 'Unranked'
                
            main_position = dict(sub['mostChampions'][0])['lane']#주포지션
            
            stats = dict(sub['mostChampions'][0])['items'][0]['stats']#세부 스탯들
            
            ob_list = ['Contribution','KDA','LaningPhase','Carry','TeamLuckRC','CSPM','GPM','CSDAt15','GDAt15','LVDAt15','KPM','APM','DEATHPM','Solokills','Solodeaths','DPM',
                'DPMPG','DPMPD','KPAt15','KP','VSPM','CWPM']#우리가 추출해야할 Key값
            
            
            platy_stats = {x['category']:round(x['value'],2) for x in stats if x['category'] in ob_list}#세부지표 숫자
            platy_top = {x['category']:round(x['top'],2) for x in stats if x['category'] in ob_list}#세부지표 동티어 백분률(상위 ..%)
            
            def abc(data):
                return [x for i,x in self.dic['stat_rank_craw'].items() if float(i)<=data][0]#SSS 혹은 A+와 같이 변환 시켜주는 함수
            
            a = ['Carry','DPM','DPMPG','DPMPD']#SSS 혹은 A+와 같이 보여야 하는 키들
            
            for i in a:
                platy_stats[i] = abc(1 - int(platy_top[i]))#백분률을 상위로 나타내어 값 변환
            platy_stats['TeamLuckRC'] = self.dic['team'][str(int(platy_stats['TeamLuckRC']))]#팀운 변환
            #이 아래는 우리 리스트 형식에 맞게 재배치
            data = [main['name'],before_season,main_position,num_game]#
            for i in ob_list:
                data.append(platy_stats[i])
            data.append(target)    
            return data
        except KeyError:
            return '소환사명 재 확인'