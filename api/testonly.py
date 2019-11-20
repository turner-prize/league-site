import sqlite3
try:
    conn = sqlite3.connect('../league.db')
    c = conn.cursor()
    m = c.execute("""select teamname from managers""")
    teamname = [row[0] for row in m]
    allDatasets = []
    
    c2 = conn.cursor()
    for name in teamname:
        x = c2.execute('select th.id,th.gameweek,th.position from tableHistory th left join managers m on th.manager = m.id where teamname = ?',(name,))
        thisDataset = []
        for irow in x:
            thisDatapoint = {}
            gw = irow[1]
            pos = irow[2]
            thisDatapoint['x'] = gw
            thisDatapoint['y'] = pos
            thisDataset.append(thisDatapoint)
        fin = {
               'label':name,
               'data':thisDataset
               }
        allDatasets.append(fin)
    print(allDatasets)
    conn.close()
    input()
except Exception as e:
    print(e)
    input()