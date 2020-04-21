from flask import *
from data_analyst import *
from flask_restplus import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wanna')
def wanna():
    return render_template('wanna.html')

@app.route('/specific')
def specific():
    return render_template('specific.html')

@app.route('/GDP-analysis/<string:city>/<string:factor1>/<string:factor2>/<string:factor3>/<int:year>')
def GDP_analysis(city,factor1,factor2,factor3,year):
    main(city,factor1,factor2,factor3)
    return 'Hello'

@app.route('/defaultanalyse',methods=['POST'])
def analysis():
    city = request.form.get('city')
    plot_url = analysisbycityname(city)
    return render_template('analysis.html', plot_url=plot_url)

@app.route('/specificanalysis',methods=['POST'])
def specificanalysis():
    factors = []
    city = request.form.get('city')
    year = request.form.get('year')
    Population =request.form.get('Population')
    Transport = request.form.get('Transport')
    Education = request.form.get('Education')
    Health = request.form.get('Health')
    Employment = request.form.get('Employment')
    Shopping = request.form.get('Shopping')

    if Population is not None:
        factors.append('Population')
    if Transport is not None:
        factors.append('Public Transport Service Mark')
    if Education is not None:
        factors.append('Education Service Mark')
    if Health is not None:
        factors.append('Health Service Mark')
    if Employment is not None:
        factors.append('Employment rate')
    if Shopping is not None:
        factors.append('Shoppingg Service Mark')

    if len(factors) > 3:
        plot_url = main(city, "Health Service Mark", 'Shoppingg Service Mark', 'Employment rate', int(year))

    if len(factors) == 0:
        plot_url = analysisbycityname(city)

    if len(factors) == 1:
        factor1 = factors[0]
        factor2 = 'Health Service Mark'
        factor3 = 'Employment rate'
        plot_url = main(city, factor1, factor2, factor3, int(year))
    if len(factors) == 2:
        factor1 = factors[0]
        factor2 = factors[1]
        factor3 = 'Employment rate'
        plot_url = main(city, factor1, factor2, factor3, int(year))
    if len(factors) == 3:
        factor1 = factors[0]
        factor2 = factors[1]
        factor3 = factors[2]
        plot_url = main(city, factor1, factor2, factor3, int(year))

    return render_template('analysis.html', plot_url=plot_url)
if __name__ == '__main__':
    app.run()
