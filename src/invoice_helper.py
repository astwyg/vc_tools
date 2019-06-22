import datetime
from docxtpl import DocxTemplate


def digital_to_chinese(digital):
    str_digital = str(digital)
    if str_digital.endswith(".0") or str_digital.endswith(".00"):
        str_digital = str_digital.split(".")[0]
    chinese = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖', '0': '零'}
    chinese2 = ['拾', '佰', '仟', '万', '厘', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1:
        jiao = bs[1]
    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)):
        if i == 0:
            r_yuan[i] += '圆'
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4:
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:3]  # 去掉小于厘之后的

    j_count = -1
    for i in range(len(s_jiao)):
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao

    last_str = ''.join(last)
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])
    return last_str


class Trip:
    def __init__(self, index=1, pre_data={}):
        self.index = index
        self.pre_data = pre_data
        self.data = {
            "j":0,
            "z":0,
            "c":0,
            "q":0
        }
        self.transport_tax = []
        self.invoice_cnt = 0
        self.invoices=[]
        self.date_ = ""
        self.start_date = ""
        self.end_date = ""
        self.from_ = ""
        self.to_ = ""
        self.didi_flag = False

        self._types = {
            "j":"交通费",
            "z":"住宿费",
            "c":"餐费",
            "q":"其他",
            "d":"滴滴票",
            "h":"火车票"
        }

    def add_invoice(self, info):
        if info[0] not in self._types.keys():
            print("类型不在下列范围\n")
            print(self._types)
            print("\n")
            return
        # TODO 检查最小到分
        self.invoices.append({
            "type": info[0],
            "money": float(info[1:])
        })

    def format_(self):
        for invoice in self.invoices:
            if invoice["type"] == "j":
                self.data["j"] = self.data["j"] + invoice["money"]
                self.invoice_cnt += 1
            elif invoice["type"] == "d":
                self.data["j"] = self.data["j"] + invoice["money"]
                self.didi_flag = True
            elif invoice["type"] == "h":
                self.data["j"] = self.data["j"] + invoice["money"]
                self.transport_tax.append(round(invoice["money"]/1.09*0.09,2))
                self.invoice_cnt += 1
            elif invoice["type"] == "z":
                self.data["z"] = self.data["z"] + invoice["money"]
                self.invoice_cnt += 1
            elif invoice["type"] == "c":
                self.data["c"] = self.data["c"] + invoice["money"]
                self.invoice_cnt += 1

        if self.data["c"] == 0:
            days = int(int(self.end_date) - int(self.start_date))
            if self.to_ == "北京":
                self.data["q"] = "补助48*{}={}".format(days, days*48)
            else:
                self.data["q"] = "补助60*{}={}".format(days, days * 60)

        return dict({
            "date": self.date_,
            "from": self.from_,
            "to": self.to_,
            "cnt": self.invoice_cnt,
            "transport_tax": self.transport_tax,
            "didi_flag": self.didi_flag
        }, **self.data)

    def start(self):
        print("第{}组行程\n".format(self.index))
        self.start_date = input("开始日期? 格式:yyyyMMdd, 如果结束请直接回车\n")
        if not self.start_date:
            return None
        self.end_date = input("结束日期?({})\n".format(self.start_date))
        if not self.end_date:
            self.date_ = self.start_date
            self.end_date = self.start_date
        else:
            self.date_ = self.start_date + "-" + self.end_date

        if self.index == 0:
            self.from_ = input("始发地?(天津)\n")
            if not self.from_:
                self.from_ = "天津"
        else:
            self.from_ = input("始发地?({})\n".format(self.pre_data.get("to")))
            if not self.from_:
                self.from_ = self.pre_data.get("to")
        self.to_ = input("目的地\n")

        while True:
            info = input("输入类型+金额\n")
            if not info:
                break
            else:
                self.add_invoice(info)

        return True


def main():
    infos = []
    trip1 = Trip(0)
    trip1.start()

    pre_data = trip1.format_()
    infos.append(pre_data)
    for i in range(1,4):
        trip = Trip(i, pre_data)
        if not trip.start():
            break
        pre_data = trip.format_()
        infos.append(pre_data)

    date=[]
    from_=[]
    to_=[]
    j=[]
    z=[]
    c=[]
    q=[]
    cnt=0
    transport_tax=[]
    money=0

    didi_flag = False
    for info in infos:
        date.append(info["date"])
        from_.append(info["from"])
        to_.append(info["to"])
        j.append(info["j"])
        z.append(info["z"])
        c.append(info["c"])
        q.append(info["q"])
        if info["c"]:
            money += info["j"]+info["z"]+info["c"]
        else:
            money += info["j"] + info["z"] + float(info["q"].split("=")[-1])
        cnt += info["cnt"]
        transport_tax = transport_tax + info["transport_tax"]
        if info["didi_flag"]:
            didi_flag = True

    if didi_flag:
        didi_tax = input("输入滴滴票税金, 用空格隔开\n")
        didi_tax = didi_tax.split(" ")
        cnt += len(didi_tax)
        for tax in didi_tax:
            transport_tax.append(float(tax))

    context = {
        "transport_tax_len": len(transport_tax),
        "transport_tax": "<w:br/>".join(str(x) for x in transport_tax),
        "date": "<w:br/>".join(str(x) for x in date),
        "from_": "<w:br/>".join(str(x) for x in from_),
        "to_": "<w:br/>".join(str(x) for x in to_),
        "j": "<w:br/>".join(str(x) for x in j),
        "z": "<w:br/>".join(str(x) for x in z),
        "c": "<w:br/>".join(str(x) for x in c),
        "q":"<w:br/>".join(str(x) for x in q),
        "c_year" : datetime.datetime.now().year,
        "c_month" : datetime.datetime.now().month,
        "c_day" : datetime.datetime.now().day,
        "money": money,
        "cap": digital_to_chinese(money),
        "cnt":cnt
    }
    doc = DocxTemplate("invoice_helper_template.docx")
    doc.render(context)
    doc.save("报销-{}.docx".format(infos[0]["date"]))

    print(infos)


def test1():
    doc = DocxTemplate("invoice_helper_template.docx")
    doc.render({
        "j":"100<w:br/>200"
    })
    doc.save("报销-test.docx")

if __name__ == "__main__":
    main()
    # test1()