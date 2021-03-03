import pandas as pd
import datetime

def get_col(param,router_id):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    #print(df.loc[1:1,router_id].values)
    df=df[df['Router_id']==router_id]
    return df["Network Health"]
#print(get_col(" ","Summary"))
def get_list_of_routers():
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    return map(str,df['Router_id'].unique())


def get_network_col():
    return 'Network Health'

def get_hardware_col():
    return 'Hardware Health'

def get_software_col():
    return 'Software Health'




def get_router_id(row):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return str(temp[row])


def get_col_group(param):

    if param == "network":
        df = ["ipv4", "ipv6", "mpls", "mac"]
    elif param == "software":
        df = ["iosd", "res", "err"]
    elif param == "hardware":
        df = ["cpu", "mem", "fan", "power", "tcam", "faults"]

    return df


def compute_score(router_id, param):

    now = datetime.datetime.now().replace(second=0, microsecond=0) - 3 * \
        datetime.timedelta(minutes=1)  # time stamp of detected cpu usage

    if (param == "summary"):
        return max(compute_score(router_id, "network"), compute_score(router_id, "hardware"), compute_score(router_id, "software"))

    # fix now
    df = get_col(param, router_id)
    print("db",df)

    if any(float(x) > 95 for x in df):
        score = 150
    elif any(float(x) > 85 for x in df):
        score = 90
    else:
        score = 30
    return score


def get_title(param):
    titles = {'cpu': 'Total CPU Utilization', 'iosd': 'IOSd Process Utilization', 'mem': 'Total Memory Utilization',
              'ipv4': 'IPv4 Route Utilization', 'ipv6': 'IPv6 Route Utilization', 'mac': 'MAC Table Utilization',
              'fan': 'Fan Speed', 'power': 'Power', 'mpls': 'MPLS Label Utilization', 'tcam': 'External TCAM(KBP) Utilization',
              'res': 'ID Allocation', 'err': 'Errors/Pending Objects', 'faults': 'Faults on the IM cards'}
    return titles[param]
