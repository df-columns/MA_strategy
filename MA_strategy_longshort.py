def MA_strategy_longshort(path, X, Y):
    # 데이터 로드. Sheet1은 TIGER 200, Sheet2는 TIGER 인버스 종가이다.
    import pandas as pd
    import matplotlib.pyplot as plt
    df=pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    dg=pd.read_excel(path, sheet_name='Sheet2', index_col=0)
    df['TIGER 인버스']=dg

    # 이평선 만들기
    df['MA'+str(X)]=df['TIGER 200'].rolling(window=X).mean()
    df['MA'+str(Y)]=df['TIGER 200'].rolling(window=Y).mean()
    
    # 매수신호, 매도신호 입력
    df2=df[Y-1:-1]
    df2['매수신호']='No'
    df2['매도신호']='No'
    df2['보유여부']='No'
    for i in range(1,len(df2)):
        if df2.loc[df2.index[i-1],'MA'+str(X)]<df2.loc[df2.index[i-1],'MA'+str(Y)]:
            if df2.loc[df2.index[i],'MA'+str(X)]>df2.loc[df2.index[i],'MA'+str(Y)]: #상방 돌파신호
                df2.loc[df2.index[i], '매수신호']='Yes'
    
    for i in range(1,len(df2)):
        if df2.loc[df2.index[i-1],'MA'+str(X)]>df2.loc[df2.index[i-1],'MA'+str(Y)]:
            if df2.loc[df2.index[i],'MA'+str(X)]<df2.loc[df2.index[i],'MA'+str(Y)]: #하방 돌파신호
                df2.loc[df2.index[i], '매도신호']='Yes'
                
    for i in range(1,(len(df2))):
        if df2.loc[df2.index[i],'매수신호']=='Yes':
            df2.loc[df2.index[i],'보유여부']='TIGER 200'
        elif df2.loc[df2.index[i],'매도신호']=='Yes':
            df2.loc[df2.index[i],'보유여부']='TIGER 인버스'
        else:
            if df2.loc[df2.index[i-1],'보유여부']=='TIGER 200':
                df2.loc[df2.index[i],'보유여부']='TIGER 200'
            elif df2.loc[df2.index[i-1],'보유여부']=='TIGER 인버스':
                df2.loc[df2.index[i],'보유여부']='TIGER 인버스'
    
    # 일간 수익률 입력
    df2['daily TIGER 200 return']=df2['TIGER 200'].pct_change()
    df2['daily TIGER 인버스 return']=df2['TIGER 인버스'].pct_change()
    
    # 시작일 구하기
    start=[]
    for i in range(len(df2)):
        if df2.loc[df2.index[i-1],'매수신호']=='No':
            if df2.loc[df2.index[i],'매수신호']=='Yes':
                start.append(i)
    
    # 포트폴리오 구성
    df2['Portfolio']=0
    df2.loc[df2.index[0:start[0]+1], 'Portfolio']=1000000
    
    # 포트폴리오 운용
    # TIGER 200 보유중일땐, 다음날부터 수익률에 영향을 받음.
    # 현금 보유중일 땐 다음날부터 포트폴리오 그대로.
    for i in range(start[0],len(df2)-1):
        if df2.loc[df2.index[i],'보유여부']=='TIGER 200':
            df2.loc[df2.index[i+1], 'Portfolio']=(1+df2.loc[df2.index[i+1],'daily TIGER 200 return'])*df2.loc[df2.index[i],'Portfolio']
        elif df2.loc[df2.index[i],'보유여부']=='TIGER 인버스':
            df2.loc[df2.index[i+1],'Portfolio']=(1+df2.loc[df2.index[i+1], 'daily TIGER 인버스 return'])*df2.loc[df2.index[i],'Portfolio']
    
    # 그림 그리기      
    df2['benchmark']=df2['TIGER 200']/df2.loc[df2.index[0],'TIGER 200']
    strategy=df2['Portfolio']/df2.loc[df2.index[0],'Portfolio']
    plt.figure(figsize=(15,10))
    plt.grid()
    plt.plot(strategy, label='strategy: MA'+str(X)+', MA'+str(Y))
    plt.plot(df2['benchmark'], label='benchmark: KOSPI 200')
    plt.legend()
    
def MA_strategy_longshort_result(path, X, Y):
    # 데이터 로드. Sheet1은 TIGER 200, Sheet2는 TIGER 인버스 종가이다.
    import pandas as pd
    import matplotlib.pyplot as plt
    df=pd.read_excel(path, sheet_name='Sheet1', index_col=0)
    dg=pd.read_excel(path, sheet_name='Sheet2', index_col=0)
    df['TIGER 인버스']=dg

    # 이평선 만들기
    df['MA'+str(X)]=df['TIGER 200'].rolling(window=X).mean()
    df['MA'+str(Y)]=df['TIGER 200'].rolling(window=Y).mean()
    
    # 매수신호, 매도신호 입력
    df2=df[Y-1:-1]
    df2['매수신호']='No'
    df2['매도신호']='No'
    df2['보유여부']='No'
    for i in range(1,len(df2)):
        if df2.loc[df2.index[i-1],'MA'+str(X)]<df2.loc[df2.index[i-1],'MA'+str(Y)]:
            if df2.loc[df2.index[i],'MA'+str(X)]>df2.loc[df2.index[i],'MA'+str(Y)]: #상방 돌파신호
                df2.loc[df2.index[i], '매수신호']='Yes'
    
    for i in range(1,len(df2)):
        if df2.loc[df2.index[i-1],'MA'+str(X)]>df2.loc[df2.index[i-1],'MA'+str(Y)]:
            if df2.loc[df2.index[i],'MA'+str(X)]<df2.loc[df2.index[i],'MA'+str(Y)]: #하방 돌파신호
                df2.loc[df2.index[i], '매도신호']='Yes'
                
    for i in range(1,(len(df2))):
        if df2.loc[df2.index[i],'매수신호']=='Yes':
            df2.loc[df2.index[i],'보유여부']='TIGER 200'
        elif df2.loc[df2.index[i],'매도신호']=='Yes':
            df2.loc[df2.index[i],'보유여부']='TIGER 인버스'
        else:
            if df2.loc[df2.index[i-1],'보유여부']=='TIGER 200':
                df2.loc[df2.index[i],'보유여부']='TIGER 200'
            elif df2.loc[df2.index[i-1],'보유여부']=='TIGER 인버스':
                df2.loc[df2.index[i],'보유여부']='TIGER 인버스'
    
    # 일간 수익률 입력
    df2['daily TIGER 200 return']=df2['TIGER 200'].pct_change()
    df2['daily TIGER 인버스 return']=df2['TIGER 인버스'].pct_change()
    
    # 시작일 구하기
    start=[]
    for i in range(len(df2)):
        if df2.loc[df2.index[i-1],'매수신호']=='No':
            if df2.loc[df2.index[i],'매수신호']=='Yes':
                start.append(i)
    
    # 포트폴리오 구성
    df2['Portfolio']=0
    df2.loc[df2.index[0:start[0]+1], 'Portfolio']=1000000
    
    # 포트폴리오 운용
    # TIGER 200 보유중일땐, 다음날부터 수익률에 영향을 받음.
    # 현금 보유중일 땐 다음날부터 포트폴리오 그대로.
    for i in range(start[0],len(df2)-1):
        if df2.loc[df2.index[i],'보유여부']=='TIGER 200':
            df2.loc[df2.index[i+1], 'Portfolio']=(1+df2.loc[df2.index[i+1],'daily TIGER 200 return'])*df2.loc[df2.index[i],'Portfolio']
        elif df2.loc[df2.index[i],'보유여부']=='TIGER 인버스':
            df2.loc[df2.index[i+1],'Portfolio']=(1+df2.loc[df2.index[i+1], 'daily TIGER 인버스 return'])*df2.loc[df2.index[i],'Portfolio']

    return str(df2.iloc[-1,9]/df2.iloc[1,9])