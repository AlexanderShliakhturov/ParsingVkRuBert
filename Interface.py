from comments import *
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("Parser.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

def get_stat():
    url = form.plainTextEdit.toPlainText()
    ans = get_all(url)
    total_number = ans.get('Positive') + ans.get('Negative') + ans.get('Neutral')
    pos_percent = str(round((ans.get('Positive') / total_number) * 100, 1)) + '%'
    neg_percent = str(round((ans.get('Negative') / total_number) * 100, 1)) + '%'
    neu_percent = str(round((ans.get('Neutral') / total_number) * 100, 1)) + '%'
    stat_list = [list(ans)[0], ans.get('Positive'), pos_percent, list(ans)[1], ans.get('Negative'), neg_percent,
                 list(ans)[2], ans.get('Neutral'), neu_percent]
    res = [str(elem) for elem in stat_list]
    result = '\n'.join(res)
    form.plaintextEdit_2.setText(result)


def get_pos():
    url = form.plainTextEdit.toPlainText()
    pos = [str(elem) for elem in get_pos_comments(url)]
    result = '\n'.join(pos)
    form.plaintextEdit_2.setText(result)
def get_neg():
    url = form.plainTextEdit.toPlainText()
    neg = [str(elem) for elem in get_neg_comments(url)]
    result = '\n'.join(neg)
    form.plaintextEdit_2.setText(result)

def get_neu():
    url = form.plainTextEdit.toPlainText()
    neu =[str(elem) for elem in get_neutral_comments(url)]
    result = '\n'.join(neu)
    form.plaintextEdit_2.setText(result)
def get_all_c():
    url = form.plainTextEdit.toPlainText()
    all_list = [str(elem) for elem in get_all_list(url)]
    result = '\n'.join(all_list)
    form.plaintextEdit_2.setText(result)


form.StatisticButton.clicked.connect(get_stat)
form.PositiveButton.clicked.connect(get_pos)
form.NegativeButton.clicked.connect(get_neg)
form.NeutralButton.clicked.connect(get_neu)
form.All_commentsButton.clicked.connect(get_all_c)

app.exec()
