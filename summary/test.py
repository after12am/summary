# -*- coding: utf-8 -*-
import urllib, sys, difflib
from extractor import extract
from datetime import datetime

testcases = []

# japanese site
testcases.append({
'uri': u'http://www.gizmodo.jp/2012/09/post_10869.html',
'title': u'今まで見た中で1番美しいタイムラプス動画（動画）',
'body': u'''
写真家で米Gizmodoの読者でもあるジョン・イークルンド（John Eklund）さんが、この桁外れに美しいタイムラプス動画を送ってきてくれました。撮影地は太平洋岸北西部です。

タイムラプス動画って正直見飽きた感がありますが、これは次元の違う美しさで感動を覚えます。メールには「2011年1月から2012年8月にかけて、おおよそ26万枚の写真を撮影して作成しました。使ったのはカメラはCanon 5D Mark IIとMark IIIでレンズは色々です。」と書いてありました。

ちなみに使ったハードドライブの容量は6.3テラバイトだそうですよ。
'''
})

testcases.append({
'uri': u'http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html',
'title': u'Webページの本文抽出',
'body': u'''
Webページの自動カテゴライズ の続き。
前回書いたとおり、パストラックで行っている Web ページのカテゴライズでは、Web ページの本文抽出がひとつの鍵になっています。今回はその本文抽出モジュールを公開しつつ、使っている技法をざっくり解説などしてみます。


本文抽出モジュール ExtractContent ダウンロード
(右クリックして「名前をつけて保存」してください)

本モジュールの利用は至極簡単。require して analyse メソッドに解析したい html を与えるだけ。文字コードは UTF-8 です。
【追記】大事なこと書き忘れ。本モジュールは Ruby1.8.5 で動作確認していますが、特別なことはしていないので、1.8.x なら動くと思います。

$KCODE="u" # 文字コードは utf-8
require 'extractcontent.rb'

# オプション値の指定
opt = {:waste_expressions => /お問い合わせ|会社概要/}
ExtractContent::set_default(opt)

html = '' # 解析対象 html 
body, title = ExtractContent::analyse(html) # 本文抽出

本文抽出時に使用するパラメータをオプション値として指定するようになっています。パラメータ値の簡単な説明はソース内に記述しています(すいません、ドキュメントが無くて)。
これらは微妙な増減で結果が大きく変わるので、waste_expressions や decay_factor, continuous_factor あたりを中心に対象とする html や処理に応じてあれこれ調節してみてください。


余談ですが、これまで大なり小なり色々なプログラムを作ってきてますが、実はライブラリの状態で公開するのはこれが初めて。正直、勝手がよくわかってません(苦笑)。
本モジュールのライセンスはひとまず BSD ライセンスとしますが、そんなわけで不都合のない範囲であれこれ変更させていただくようなこともあるかもしれません。あしからずご了承ください。


さて。
パストラックの本文抽出は大きく以下の方針で開発しています。
- 本文を抽出する、というより「本文以外を除外する」
- カテゴライズ精度の向上に寄与する方向でのチューニング。
- 実用本位。極力一般化するが、無理な範囲はプラグインでサイト別に各種ルールを記述。
プラグインでサイト別に記述する、なんてのは誰でも出来る話なので、以下で解説するのは一般的な html に対する本文抽出ロジックに関する工夫のあれこれです(公開したモジュールもちょうどその範囲)。

まず、手を付けるに当たって参考にさせていただいたのが下記記事です。ありがとうございます。

ブログの記事本文を抽出するスクリプトをつくってみた - zuzara
http://blog.zuzara.com/2006/06/06/84/
ブログの本文抽出にチャレンジ - Ceekz Logs
http://private.ceek.jp/archives/002039.html

正確にはこれらの記事を参考に奥さんが作った本文抽出モジュール(Perl版) が社内に転がっていたので、そちらを参考にさせてもらったんですが(笑)。サイボウズ・ラボはそんなところです。はい。


そんなこんなで今回のモジュールで採った方式は下記の通り。

- div, td で囲まれた範囲をテキストブロックとして取り出す
- 句読点の数をそのテキストブロックのベースのスコアとする
- リンクタグ以外のテキスト長の割合をスコアに反映
- 前半のブロックほどスコアが高くなるように傾斜（ここまでが参考にさせていただいた部分)
- 特にリンクリストを判定し、除外する方向でスコアに反映
- アフィリエイトリンク、フォーム、フッタ等に特有のキーワードが含まれていれば、除外する方向でスコアに反映
- スコアの高い連続ブロックをクラスタ化し、クラスタ間でさらにスコアの比較を行う
- (裏技) Google AdSense Section Target を考慮

Web ページにはメニューとかヘッダーとかフッターとかプロフィールとか連絡先とかコメント欄とかトラックバックとか広告とか、とにかく本文以外の「ゴミ」がわんさかついているので、本文を抽出するというより「いかにゴミを取り除くか」に注力しています。
そういった「ゴミ」にはリンクが整列している場合が多いので、リンクリストを判定する方法を３通りほど用意して極力除外。
また広告はアフィリエイトの有無、コメントや検索はフォームの有無、フッターは特徴的な語句が含まれているかで判定できる可能性がある程度あるので、それらも判定。
語句を指定してしまうと当然ながら言語に依存してしまいますが、今回の目的はカテゴライズであり、そのフィルタは日本語に特化して学習しているので、パストラックのカテゴライズでは割り切って日本語の語句をびしばし指定して利用しています。


上にも書きましたように、コメントやトラックバックについても極力除外する方向で開発・チューニングしています。
これらを本文に含めるか含めないかは意見の分かれるところでしょうが、今回の目的はカテゴライズなので、それらはノイズだと判断しました(実際、コメント/トラックバックを含めてしまうと分類精度が落ちてしまうことがわかっています)。
逆に、全文検索のための本文抽出であればコメントやトラックバックも含めたいということも考えられますから、そこは本文抽出のロジックやチューニングに対してケースバイケースが求められる部分になるんじゃないかと思います。


また、評価の高いテキストブロックが連続している場合、それらをひとかたまりにして扱うようにしています。
本文に該当する部分が div や td で区切られてしまっていても(実際、写真の挿入や段組などのために区切られてしまうことが多々ある)、基本的にはそれらは連続していることを反映する形です。
これにより、本文の左右にある比較的文章量の多いテキストブロック(例えばアブストラクト付きの関連ページリンクなど)などを除外しています。


Ceekz さんの書かれていた、

- 直前のエントリと diff を取る
- RSS の description と比較する

あたりのアイデアにも興味はあったんですが、前者はコストが高く、後者は対象として非ブログの方が多いことが想定されたため費用対効果が低く、とりあえずスルー。


で、ここまででもカテゴライズを対象とした場合には実用レベルの本文抽出にたどり着けているのですが。
実は結構強力な裏技がありまして。


Google AdSense が表示する広告は、内容との関連性を高いほど広告効果も高まることが期待されるわけですが、それを支援するために セクションターゲット という仕組みがあります。
これはページ内で「強調したいテキスト」を <!-- google_ad_section_start --> ～ <!-- google_ad_section_end --> などで囲うことで、Google AdSense が表示する広告と照合する際に考慮する、というもの。
それってなんて本文？　なわけで、セクションターゲットに対応しているサイトであれば 100% に近い精度で本文が抜けます。
とりあえず目立つ範囲だけでも asahi.com, livedoor, hatena, gigazine, nikkeibp, mycom, nikkansports, sponichi, fc2.com, atwiki などなどなどなど、かなり多くのサイトが対応しており、今後も増えていくことが予想され(この本文抽出モジュールを作り始めたときはセクションターゲット使ってなかったはずなのに、現在は使っているというサイトがいくつか)、裏技といいつつ本文抽出やるなら見逃せない。
本当に、お金の力は偉大やのう。


ちゃんと母集団を決めて統計をとったりまではしていないのであくまで感覚的な数字ですが、オプション値をチューニングして使えば、ニュース系のサイトの記事ページなら 95%～99% 程度は期待したとおりの本文が抽出できています。
ブログはやはり千差万別なため少し厳しいのですが、それでも 90% は超えているかと。
一方で、一覧系のページ(特にポータルトップ)はもともと本文と言える部分がないに等しく、それを「本文無し」と判定してくれれば御の字なのですが、やはりどうしてもゴミっぽいところを誤って抽出してしまうことはある程度発生してしまっています。そのあたりはまだ課題ですね～。
'''
})

# english site
testcases.append({
'uri': u'http://capturevision.wordpress.com/2009/08/05/music-visualizer-progress/',
'title': u'Music visualizer progress',
'body': u'''
Actually something pretty cool happened today.. I wanted to control the sketch params with a GUI, so I quickly coded one with controlP5 that was sending OSC messages to the rendering sketch..
I soon found that controlling with the mouse was messing with the whole live feeling of the thing so I got an OSC-enabled app (no ads here  on my iPhone, and as I’m talking, I can control half of the sketch params just pushing buttons and sliders on my iPhone..

Sometimes life is cool 

So I’m slowly working my way to the music visualizer I had in mind (but the path is steep)..
'''
})

testcases.append({
'uri': u'http://www.dasprinzip.com/prinzipiell/2012/04/03/shaders-in-their-natural-habitat-episode-1/',
'title': u'Shaders in their natural habitat. episode 1',
'body': u'''
Feels like ions of years have past since I wrote some´ here (shame on me for being such a lazy bum) - but finally…
First of all, lotsa things changed during the last half year. Flash is dead… ehhhrrrr not so dead yet, HTML5 becomes the superperformant ‘jack of all trades device’ (oh yeah!) and WebGL runs on the IE (NOT). But seriously, personally I decided to give it a try and going freelance with my pet subject… a.k.a taking client-orders of projects that are in the need of Shaders (gimme gimme - frank [at] prinzipiell [dot] com).
Programming ‘just’ Shaders, wtf !!! (you´d almost think…)
But believe it or not, nowadays, it´s hardly not possible to imagine 3D-Engines/Games, programs or projects without the use of a single Shader. A Shader… what is it? To put it simply: Shaders are simple programs that describe the traits of either a vertex or a pixel (fragments). Shaders are used to program the graphics processing unit (GPU) programmable rendering pipeline and are used to primarily calculate rendering effects on graphics hardware with a high degree of flexibility.
Fair enough, but lets specify a little scope of application: Back in the good old days graphics were done in software (Hello Flash10). This might be flexible as well, but is not really performant and not very efficient because the fixed pipeline is rather limited. Something as simple as Phong-Shading already requires a shader (the shading capabilities of the fixed pipeline end with Gouraud-Shading). The possibilities that open up with shaders are huge. Some of them are: better shadowing-techniques, ambient-occlusion, normal-mapping, etc. … in other words and to say it exaggerated (!!!) modern 3D/2D-Engines/Games would look a bit lame (not to say like crap) without Shaders.
In my case, when I´ve some spare time left, I like to program more ‘experimental’ stuff with Shaders. Sound-reactive visualizations driven by WebGL f.e., like that little thingy here:

Launch (needs an WebGL enabled browser)
Or image processing stuff by combining Flash and Pixel Bender (Adobe´s ‘almost’ on GPU but in case Flash <11 on CPU shading solution):

Launch
Usually I don´t care for the language in which a Shader must be programmed (GLSL, HLSL, Pixel Bender shizzl or Assembler, sorry, I meant AGAL assembly source code for the use with Flash11), because it all depends on the target environment. When it comes to offline tasks, there are two top dogs to go for: The official OpenGL and OpenGL ES shading language is GLSL (OpenGL Shading Language), and the official Direct3D shading language is HLSL (High Level Shader Language). In case of online-usages for the internet, you can program GLSL based Shaders via WebGL for example… and, “um, errrrr…”, you could use Flash as a weapon of choice which now has GPU acceleration too (thank you Adobe, by nature the average Flash Developer likes to deal with Assembler code…).
So, “Yes M´am…”  Shaders for 3D stuff and games, but when it comes to ‘real’ projects, Shaders can be more than helpful too, doing all that nifty tasks that need performance and speed. As an example, the ‘Samsung Notasso‘ campaign I was envolved in last winter. The nice people from the Amsterdam based agency Code D’Azur contacted me to write a bunch of Pixel Bender-based plugins to use with Flash for that project, that will do all the heavy and time-critical image processing stuff: Like automated face detection, automated cutting out detected faces from the image´s background and transform every single copy into a unique piece of art (kinda). Donkey work(!), ´cause cutting out faces automatically by preventing as much face-details as you can, a.k.a hairs, contours, neck a.s.o is not trivial at all, and doing this in Flash10 Pixel Bender non-GPU-accelerated truely IS madness… but in the end, manageable! We separated the Shader-tasks into two Plugins, one to be called ‘The Scanner’, which does all the face-detection and validation whether we detected a good face-shot or not. The second Plugin I called ‘The Composer’, which does all the hard work distributed on many little single Shader tasks (like one for edge-detection, one for skin prevention, one for the actual cut-out of the face, one for contour recovery, and many more…)
You can give it a try here:

Launch
That´s it so far… the idea is to continue this article by giving you an extract from my last projects and works and to show the diverse usage of Shaders there. So this was ‘Episode 1‘ - up next… Shaders really like Dubstep, watch out!
Edit: Wanna see and know more about Shaders? Me is doing a session at upcoming ‘Beyond Tellerrand‘ conference in Cologne (is the place to be) bringing along all new fresh stuff and experiments, so maybe see you there…
'''
})

testcases.append({
'uri': u'http://www.generatorx.no/20101217/abstrakt-abstrakt-jorinde-voigt/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+generatorx+%28Generator.x%3A+Generative+strategies+in+art+%26+design%29',
'title': u'» abstrakt Abstrakt: Jorinde Voigt',
'body': u'''
Jorinde Voigt: Territorium (4), VI/aus: Position 1-x; Nord-Süd-Achse; Zentren A-Z; Position-Zentrum/Identisch; Territorium 1-x; Zentrum 1-x; N,S,W,O; Drehrichtung der Himmelsrichtung im Verlauf; Konstruktion; Dekonstruktion; Countup-Countdown-Loop: 1-x Tage; Kontinentalgrenze
Rome, 2010
70×100cm, ink, pencil on paper, signed original

The drawings of Jorinde Voigt are means to project order onto her environment. She formalizes and orders aspects, objects and impressions to form complex graphs, applying both objective (scientific) methods and subjective decisions. The system designs thus bear a scientific character, but upon closer inspection they can neither be generalized nor be deciphered in terms of applicability. The drawings constitute ’subjective abstractions’ that can only be read as aesthetic products, as symbols for the time’s penchant for formalization, and as such elude any concrete application as patterns or logic.

This text is taken from the NODE10 catalogue, written by Eno Henze and Marius Watz and edited by Valérie-Françoise Vogt. Please read the introductory curator text for an overview of the exhibition topic.
'''
})


def calculate_score(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# has similarity if scores greater than 0.6.
def evaluate(expect, res, threshold = 0.6):
    # calculate title similar rate
    score = str(calculate_score(expect['title'], res['title']))
    if score > threshold:
        title_score = '\033[36m' + score[:6] + '\033[0m'
    else:
        title_score = '\033[31m' + score[:6] + '\033[0m'
    # calculate body similar rate
    score = str(calculate_score(expect['body'], res['body']))
    if score > threshold:
        body_score = '\033[36m' + score[:6] + '\033[0m'
    else:
        body_score = '\033[31m' + score[:6] + '\033[0m'
    print '[%s] title match score: %s, body match score: %s' % \
        (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), title_score, body_score)

def main():
    for testcase in testcases:
        print '[%s] %s %s' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '\033[35m' + 'testing' + '\033[0m', testcase['uri'])
        evaluate(testcase, extract(urllib.urlopen(testcase['uri']).read()))

if __name__ == '__main__': main()