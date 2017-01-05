import pandas as pd
import datetime
import requests
from io import BytesIO, StringIO
import os
import click
import re

# the data we already cache in the package
in_package_data = range(2002, 2017)

DONWLOAD_URL = "http://yield.chinabond.com.cn/cbweb-mn/yc/downYearBzqx?year=%s&&wrjxCBFlag=0&&zblx=txy&ycDefId=%s"
YIELD_MAIN_URL = 'http://yield.chinabond.com.cn/cbweb-mn/yield_main'

def get_data():
    """
    every body need to update the new data every day,
    if you wanna cal this function multi-time intra-day, you should cache it your self


    Data are combined with 2 parts
    1 the xlsx files inside the package
    2 newly fetched data those not in the package, we will fetch them on the fly
    """
    cur_year = datetime.datetime.now().year
    last_in_package_data = max(in_package_data)

    # download new data
    to_downloads = range(last_in_package_data + 1, cur_year + 1)

    # frist, get ycDefIds params
    response = requests.get(YIELD_MAIN_URL)
    matchs = re.search(r'\?ycDefIds=(.*?)\&', response.text)
    ycdefids = matchs.group(1)
    assert (ycdefids is not None) # 如果这里失效了,请在github上联系我

    fetched_data = []
    for year in to_downloads:
        print('Downloading from ' + DONWLOAD_URL % (year, ycdefids))
        response = requests.get(DONWLOAD_URL % (year, ycdefids))
        fetched_data.append(BytesIO(response.content))

    # combine all data

    dfs = []

    basedir = os.path.join(os.path.dirname(__file__), "xlsx")

    for i in in_package_data:
        dfs.append(pd.read_excel(os.path.join(basedir, "%d年中债国债收益率曲线标准期限信息.xlsx" % i)))

    for memfile in fetched_data:
        dfs.append(pd.read_excel(memfile))

    df = pd.concat(dfs)

    return df

def get_pivot_data():
    """
    pivot data
    """
    df = get_data()
    return df.pivot(index='日期', columns='标准期限(年)', values='收益率(%)')

def get_zipline_format():
    pivot_data = get_pivot_data()
    all_china_bond = pd.read_csv(StringIO(pivot_data.to_csv()),
                                 parse_dates=['日期'],
                                 usecols=('日期', '0.08', '0.25', '0.5', '1.0', '2.0', '3.0', '5.0', '7.0', '10.0', '20.0', '30.0'))
    all_china_bond.columns =['Time Period', '1month', '3month','6month', '1year', '2year', '3year', '5year', '7year', '10year', '20year', '30year']
    all_china_bond.set_index(['Time Period'], inplace=True)
    return all_china_bond

@click.command()
@click.option("-f", '--fileformat', type=str, default='zipline',
              help='zipline (default) - zipline style file , all - dump all file')
@click.argument("path_to_save")
def save_zipline_file(fileformat, path_to_save = None):
    """
    Save china treasury curve data to file
    """
    if path_to_save is None:
        raise Exception("please provie path")
    if fileformat not in ('zipline', 'all'):
        raise Exception("filetype must in ('zipline', 'all') ")

    click.echo("saving data")
    if (fileformat == 'zipline'):
        get_zipline_format().to_csv(path_to_save, ignore_index=True)
    else:
        get_pivot_data().to_csv(path_to_save, ignore_index=True)
    click.echo("done")

if __name__ == '__main__':
    save_zipline_file()
