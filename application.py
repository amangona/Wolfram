from flask import Flask, request, jsonify
import wap

application = Flask(__name__)


API_URL = 'http://api.wolframalpha.com/v2/query.jsp'
WA_APP_ID = 'T4V4XY-82RGQ926U9'

waeo = wap.WolframAlphaEngine(WA_APP_ID, API_URL)

def get_results(equation):
    queryStr = waeo.CreateQuery(equation)

    wap.WolframAlphaQuery(queryStr, WA_APP_ID)
    result = waeo.PerformQuery(queryStr)
    result = wap.WolframAlphaQueryResult(result)

    data = []
    answer = []
    for pod in result.Pods():
        waPod = wap.Pod(pod)
        title = "Pod.title: " + waPod.Title()[0]
        print title
        for subpod in waPod.Subpods():
            waSubpod = wap.Subpod(subpod)
            plaintext = waSubpod.Plaintext()[0]
            img = waSubpod.Img()
            src = wap.scanbranches(img[0], 'src')[0]
            alt = wap.scanbranches(img[0], 'alt')[0]
            print "-------------"
            print "img.src: " + src
            image = "img.src: " + src
            data.append(src)
            answer.append(plaintext)
            print "img.alt: " + alt
        print "\n"

    return data, answer


@application.route('/get-answers', methods=['POST'])
def get_answer():
    data = request.get_json()

    equation = data.get('equation')
    data = get_results(equation)

    return jsonify({'URLS': data}), 200


if __name__ == '__main__':
    application.run(debug=True)
