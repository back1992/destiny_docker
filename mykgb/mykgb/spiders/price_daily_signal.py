# -*- coding: utf-8 -*-
import scrapy
from myapp.models import *
from mykgb.items import *
import talib
from mykgb import indicator


class PriceDailySignalSpider(scrapy.Spider):
    name = "price_daily_signal"
    allowed_domains = ["www.sina.com"]
    start_urls = ['http://www.sina.com/']

    def __init__(self, msg_cc='', *args, **kwargs):
        # self.msg_cc = "280037713@qq.com"
        self.receiver = "13261871395@163.com"
        self.msg_cc = ""

        super(scrapy.Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # Signal.objects.all().delete()
        Signal.objects.update(macd=0, kdj=0, rsi=0, cci=0)
        codes = Codeset.objects.filter(actived=True)
        # codes = Codeset.objects.filter(codeen='A')
        for code in codes:
            qs = Price.objects.filter(code=code).order_by('date')
            df = qs.to_dataframe(index='date')
            macd = indicator.get_macd(df)
            kdj = indicator.get_kdj(df)
            rsi = indicator.get_rsi(df)
            cci = indicator.get_cci(df)
            signal, created = Signal.objects.update_or_create(code=code)
            signal.macd = sum(macd.values())
            signal.kdj = sum(kdj.values())
            signal.rsi = sum(rsi.values())
            signal.cci = sum(cci.values())
            signal.save()
        signal_msg = self.send_signal()
        # sm("最新版内盘信号", signal_msg, self.receiver, self.msg_cc)

    def send_signal(self):
        signal = ''
        df = Signal.objects.all().to_dataframe()
        df['signal'] = df['macd'] + df['kdj'] + df['rsi'] + df['cci']
        df = df[df['signal'] != 0].sort_values(by=['signal'], ascending=[-1])
        print(df)
        for index, row in df.iterrows():
            if row['signal'] <= 0:
                signal += u'<h3 STYLE="color:green;">做空 ' + row['code'] + u'强度：' + str(row['signal'])
                '</h3>'
            else:
                signal += u'<h3 STYLE="color:red;">做多 ' + row['code'] + u'强度：' + str(row['signal'])
                '</h3>'
            signal += '<p>' + '  macd:' + str(row['macd']) + '  macd:' + str(row['kdj']) + '  kdj:' + str(
                row['macd']) + '  rsi:' + str(row[
                                                  'rsi']) + '  cci:' + \
                      str(row['cci']) + '</p>'
        return signal
