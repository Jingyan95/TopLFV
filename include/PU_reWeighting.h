#ifndef MY_PU
#define MY_PU
#include <iostream>
#include <TString.h>
#include <cassert>
//Taken from Reza: https://github.com/rgoldouz/ExcitedTopAnalysis/tree/main/NanoAnalysis
class PU {

public:

  PU();
  virtual ~PU();
  double PU_2016preVFP(int, TString);
  double PU_2016postVFP(int, TString);
  double PU_2017(int, TString);
  double PU_2018(int, TString);
  double getPUweight(TString, int, TString);

private:

  double puUL2017_up[74] = {
  0.5282557242575738, 0.6443592344302421, 0.43563214010334583, 1.232896217164608, 0.6813120196604882, 0.8173814259660118, 0.9699813077835107, 0.8474407889588852, 0.5507151111500969, 0.4610690470979574, 0.5342559339397746, 0.5669717253577361, 0.6342341740476306, 0.6532065806073212, 0.6457531425580176, 0.6379748800874974, 0.6526294707631506, 0.6894995914909015, 0.7374308957303126, 0.7766160404650421, 0.8149430503821287, 0.8510646529987701, 0.8780490300670013, 0.8933844319160602, 0.8956851540005754, 0.8961636162370954, 0.9014063315720203, 0.9177949687620252, 0.9407892483240936, 0.9670743354301816, 0.9964279197244451, 1.0270404301285148, 1.058417922199154, 1.0940684931043674, 1.1266211147571203, 1.1550058009844717, 1.1773461081114116, 1.19002632974587, 1.1926558056456105, 1.1774322105360644, 1.1389529526742135, 1.089654411220591, 1.0225471669032766, 0.9495554136022775, 0.8836902201634372, 0.849821443049736, 0.8451006412390613, 0.8750286149777811, 0.9322782302400893, 1.037995120410628, 1.20385023508006, 1.3998994565687042, 1.6277764227082487, 1.8767738807016803, 2.0781446144210345, 2.2990245144156205, 2.509695968271518, 2.737834366111124, 3.0210532030385733, 3.379485145414457, 3.760579569410429, 4.177536942510479, 4.621195636465452, 5.0730962013275995, 5.532517465565883, 5.96958197126759, 6.839771128463083, 9.786042789267452, 14.126715488916405, 13.66117225021312, 21.332145854524047, 62.49610405160676, 113.12326622282671, 591.6532323992939};

  double puUL2017_down[74] = {
  0.5978281528668126, 0.8076880038977378, 0.7068453150098031, 1.1679782695077312, 0.9349064756021407, 1.015247321531873, 1.0473850508680527, 1.0350985397377506, 0.9933875538753418, 1.0624124967369497, 1.0984165822159484, 1.1376685604547145, 1.0986157781503585, 1.116458198743941, 1.1267868333091087, 1.1370550558247303, 1.1452283443626194, 1.1309280395822234, 1.1201867870054656, 1.1079937295068154, 1.099346537450643, 1.0917169555219606, 1.0839876993494504, 1.0777132618120815, 1.0688986772011326, 1.0591336378126952, 1.0446263943234875, 1.0307156240319932, 1.016090066100545, 1.0019247061887555, 0.9908169496137268, 0.9804498877706953, 0.9690699386294302, 0.9613010709940994, 0.9547044344401384, 0.9521451385331152, 0.9537582488028427, 0.9587155396223985, 0.9719441910095509, 0.9945388508187331, 1.0261060788149405, 1.0728790216369732, 1.110972277660298, 1.1248587422656022, 1.103499385307187, 1.064606519223383, 1.0041279060479837, 0.9337611622773759, 0.852427917995906, 0.7840809057977479, 0.7321660951201953, 0.6748912756573122, 0.6182854103378955, 0.5625684275458129, 0.4955872581218579, 0.44199664322458215, 0.3955699716443741, 0.36051839883864883, 0.3389641491287525, 0.32952266487379533, 0.3248907177047022, 0.32592177688325463, 0.33180424640120304, 0.34167247159470937, 0.3562480242168431, 0.3743807862895801, 0.42493475498545946, 0.6108720514583721, 0.8950998123467349, 0.8834194780841488, 1.4085645361322552, 4.196657947109761, 7.666078258546679, 40.053449224671354};

  double puUL2016preVFP_up[80] = {
  0.20934728710341283, 0.328546808598741, 0.7531578181753131, 0.8672641935378242, 1.121822060185732, 1.3706285372058915, 1.46375541919262, 1.1482929300498088, 0.9557057999967602, 0.9037675362136479, 0.8933280637745505, 0.879985310363961, 0.8662579400175133, 0.8625700085046069, 0.8744546114878246, 0.9100786476862833, 0.9562535760548061, 0.9990650136020425, 1.0312476323078221, 1.050579784570688, 1.0569352449072162, 1.0567237256498705, 1.0573941286869195, 1.0608538869436899, 1.062624262226345, 1.0608476992789149, 1.051759611872856, 1.0356932484685466, 1.0148541101107802, 0.9910927107029619, 0.9651050319501678, 0.941670385681263, 0.9261260436691636, 0.9194074665198904, 0.9194329516909558, 0.9243334348463493, 0.9381437534313571, 0.956598297269418, 0.9843410322115854, 1.0197812455102393, 1.0634560141010847, 1.1225208585217512, 1.206592075683282, 1.3228046731054754, 1.4842998031344774, 1.6583738248821727, 1.8826612751572633, 2.1656084808372738, 2.414750511834853, 2.6178458726339566, 2.714986591165414, 2.762435031967652, 2.586747367566336, 2.4253556233984312, 2.11655680507759, 1.5899876465599427, 1.2896158194805412, 0.8275616345597236, 0.7186551751297467, 0.5420098347328581, 0.3820273504996547, 0.3004847481821305, 0.2773108192233316, 0.2143809278461138, 0.11375350816508223, 0.07317975145837637, 0.11132713873992978, 0.07708350499751666, 0.05143178955581515, 0.15332917842481203, 0.24403218965589538, 0.023255264279311738, 0.023506163184895148, 0.1424896278907382, 0.05119540355263701, 0.0043613033323046755, 0.027899624405544846, 0.010177914497650707, 0.0018600286999679244, 0.00018740050984062043};

  double puUL2017_nominal[74] = {
  0.5606274531031112, 0.7356768448138682, 0.5379188426448102, 1.2182340490089563, 0.8022589335878173, 0.9162976579339998, 1.003535297339447, 0.9251530005613752, 0.6846759067725198, 0.7131643259598123, 0.7505121360758453, 0.8165177069280811, 0.8376691182629196, 0.8463556632882329, 0.8440283058630812, 0.8439067805634669, 0.8666288079994602, 0.8929616452906328, 0.9180239787579902, 0.9357902581699746, 0.9556426537184208, 0.972143647981642, 0.9811830177589081, 0.9832298066767534, 0.9780842729569711, 0.9759522364261591, 0.9765532546498046, 0.982684532458617, 0.9903925626548388, 0.9981198259762551, 1.0078237725887502, 1.0190171556865095, 1.0302623764785477, 1.0435067370186102, 1.0528812746193779, 1.0608328118324004, 1.0679579498849403, 1.0711178329087099, 1.070172628103765, 1.060859315173904, 1.0426792366069437, 1.0292999129487364, 1.0110271247401585, 0.9897588281162832, 0.9667127912205582, 0.9596532370954036, 0.9605181711699639, 0.9726212316412776, 0.985980282438256, 1.020363707245282, 1.0798058357556355, 1.1309572028312935, 1.1752437206584858, 1.2064250195347632, 1.1893481947111917, 1.1753639170378514, 1.153045701742742, 1.1393426183396158, 1.1491058997866475, 1.1861940242320668, 1.2296909774222218, 1.2843317626465525, 1.3475112340267736, 1.4150772055542293, 1.4889932386254965, 1.5639928112244066, 1.7605077201696253, 2.4973721771534363, 3.6048463912894864, 3.5103704309978547, 5.546157726604595, 16.47348645728898, 30.208288447631777, 159.55129944394523};

  double puUL2016preVFP_down[80] = {
  0.27720048855454993, 0.4471434220529028, 0.9616765511614401, 1.1495792395055036, 1.866909952277629, 2.665150398378626, 2.27975982796461, 1.7410107095107588, 1.608098567324491, 1.5510014950784876, 1.4756370789384075, 1.3931581130193562, 1.3388181592382669, 1.3100288058359295, 1.2850712851695345, 1.256424191622392, 1.2280026966342554, 1.205792223381641, 1.1804727168505047, 1.1496607851873024, 1.1146934657755152, 1.0778304651356057, 1.0398145195199013, 0.9982340144642435, 0.9487914341887876, 0.8929525234272376, 0.8318727261577847, 0.7698739356835256, 0.7109743581834089, 0.6568329462261578, 0.6066716500754626, 0.5612270302087623, 0.521034237372348, 0.48436166410824916, 0.44891075502628514, 0.41365107884153596, 0.38079490699865515, 0.34898897861877476, 0.3203773105244379, 0.29439177212464185, 0.2710867824714042, 0.2518244227570226, 0.2376177864827248, 0.2282337086282719, 0.22401705015069007, 0.2186343373678791, 0.21654226677564434, 0.2170779562595744, 0.21079601022990477, 0.1990262721289443, 0.18002886615169203, 0.160361169040392, 0.13239754905630308, 0.11072926540403022, 0.08767370419238973, 0.06112401857108536, 0.047278022942703654, 0.029786359811224964, 0.026093761097032802, 0.02027400759914089, 0.01489458188625766, 0.012225747918078947, 0.011675388586891707, 0.009195761266136575, 0.004875985710606027, 0.0030726345105632443, 0.004495741939153, 0.0029481966890081974, 0.0018403452921620118, 0.0050844738375731184, 0.007444333998152405, 0.0006487716566323712, 0.0005967047915017346, 0.0032762629133866873, 0.0010615154963014943, 8.118822833500156e-05, 0.0004641975939263875, 0.00015065818448476974, 2.1486853459520697e-05, 1.8987870924737154e-06};

  double puUL2018_down[79] = {
  5.142728966511908, 1.252340989572891, 1.460147842908786, 1.0309886851193482, 0.8940347955181891, 1.1795670295340732, 1.5657325467748122, 1.600282068492879, 1.3279383511067466, 1.116432636672774, 1.028541999016465, 1.0120671758259054, 1.0054908707676666, 1.0262952248285369, 1.0569706049517966, 1.083516338908162, 1.0967559399158024, 1.0971860185110618, 1.0959033583097137, 1.1031846312902935, 1.1105755357489062, 1.1076766763752388, 1.1002374522836504, 1.0946506153542315, 1.0853547864968809, 1.0738025022416233, 1.063184513328571, 1.0639711436475228, 1.0690187754024034, 1.0731227628319953, 1.074572813846724, 1.0717589477703506, 1.0643873558533956, 1.0542315241293436, 1.0403751646340058, 1.0232438876597723, 1.0023033740252596, 0.9783363264852963, 0.9504741047733934, 0.9209968666426794, 0.8896969922411466, 0.8565765392375986, 0.8227400771953568, 0.78869880090806, 0.7529865451376058, 0.7194939813956848, 0.6880411815639504, 0.6591463558118369, 0.6326012677013659, 0.606410755447268, 0.5837688926925418, 0.5619730415824356, 0.5418326722191936, 0.528838547849688, 0.5093433172460948, 0.49132561745380343, 0.4733166444392937, 0.4634091634851133, 0.4490682742246927, 0.4377015888292496, 0.42218665794650656, 0.3968928267765089, 0.3552228889899212, 0.3097935105166106, 0.27167180388703577, 0.2317217137791456, 0.2054132189260335, 0.17566968920824183, 0.13896710636052406, 0.1255068082476665, 0.11219688744322265, 0.12601438405659524, 0.11881449935348361, 0.08375492532479671, 0.060007816857724675, 0.05885399083405891, 0.056690317473146845, 0.05284452099556204, 0.1147115895713905};

  double puUL2016postVFP_down[80] = {
  0.3181096494212727, 0.4258472308048462, 0.9716377453073761, 0.7741129354002586, 0.6966959569039752, 0.37424129818360924, 0.17780181411705123, 0.152158711461441, 0.14570024098330558, 0.22588717239984255, 0.3929511033769083, 0.5611572549617997, 0.6781905137733656, 0.7452822028402328, 0.7832056949805093, 0.8108377733378852, 0.8320442645349115, 0.852068241928513, 0.8736123845761338, 0.9006108718052432, 0.9345493780730355, 0.9722816204661568, 1.0100919960020391, 1.0479929394038667, 1.0868902133721914, 1.1300726188624517, 1.1748246138745546, 1.219151876264125, 1.2613429716612496, 1.2984183162301162, 1.3254830436774094, 1.3436630082036534, 1.3565937290771428, 1.3632348900165596, 1.359114612364189, 1.3406982133291572, 1.313331964785979, 1.27029302166429, 1.2171334736610846, 1.1509042156471077, 1.0722101795711505, 0.9883759082395999, 0.9061667434353022, 0.8272853690562044, 0.7549451661412601, 0.6707313019541254, 0.5934729954300846, 0.5237079825456702, 0.4439628311129133, 0.36649245501894673, 0.294398267067712, 0.24087886325842467, 0.1926437509240209, 0.16683710454491166, 0.1462613005202121, 0.11894171699063277, 0.11044474646551046, 0.08404633013637633, 0.08803464843662268, 0.08027536268132468, 0.0677834380082751, 0.06272089577612973, 0.06643591680690228, 0.05729554723915856, 0.032934707768644975, 0.02232469164175724, 0.034922284801587454, 0.02436495335574805, 0.01611841017980597, 0.047049259524631015, 0.07261462124325423, 0.006660665526131353, 0.006442803865136863, 0.03720220033661371, 0.012685006492769652, 0.0010224302491406722, 0.00617312047840708, 0.0021212956676526368, 0.0003425652984145965, 3.240348804667767e-05};

  double puUL2016preVFP_nominal[80] = {
  0.23968425612147268, 0.38207211127077784, 0.8493669530932791, 0.9919686071278767, 1.4104117344427771, 1.9140019304969131, 1.8432342460015436, 1.3940420660049047, 1.2240401254860975, 1.179250595035078, 1.1482839840804144, 1.1062798265944762, 1.0741460982957787, 1.0612285690178982, 1.06383812613343, 1.0796728392514052, 1.094720153312641, 1.1077636935523918, 1.1133617917710275, 1.1079484702449636, 1.0934197420977987, 1.075862747403851, 1.0595922886864142, 1.0433969129745548, 1.021580907856282, 0.9930754253871723, 0.9562122182698554, 0.9136319831399353, 0.8692264045897413, 0.8256087581074498, 0.7834483301580112, 0.7458117262691689, 0.7152962567136668, 0.6907392347367843, 0.6691099225301076, 0.6482331274475904, 0.6306243107400402, 0.613308719088505, 0.5994001719545634, 0.587791213291866, 0.578673006626597, 0.575483704415566, 0.5819250639914461, 0.5994815626834529, 0.6315307386986713, 0.6619717918895339, 0.7046011846183657, 0.7594716689864025, 0.7930920699370176, 0.8048441991029206, 0.781174176924098, 0.7440240848613285, 0.6528726321208682, 0.5749914013960602, 0.47333479763501984, 0.33766315350394055, 0.26257211074398346, 0.16357043708449764, 0.13994174468942425, 0.10559939625175213, 0.07549831654461307, 0.06080675714172643, 0.05765661738673498, 0.045662716419438074, 0.024628245806930984, 0.015935830032518392, 0.024115218713516035, 0.016443218443816767, 0.010714758446501207, 0.03099580593889563, 0.04763842446570458, 0.004368169671474522, 0.004236640131757176, 0.024586208104864234, 0.008439582916180056, 0.0006855463955203526, 0.004173423657537548, 0.0014459185008298587, 0.00023681899274470705, 2.2513309902757976e-05};

  double puUL2016postVFP_up[80] = {
  0.24409000969267947, 0.2895226873225315, 0.8507172262014899, 0.6287115689100693, 0.5800534742947709, 0.31077219343965573, 0.14819107651114444, 0.08596214721661732, 0.08724588990780731, 0.08356423345775704, 0.13537016420651918, 0.23151922582969137, 0.33699404906991004, 0.4227011189583685, 0.48492906729631363, 0.5419679508258012, 0.60152059743616, 0.6599899866706512, 0.7096616243770221, 0.7512490271196723, 0.7897906760969897, 0.8329749856209115, 0.8871827372370165, 0.9515372567942099, 1.0195794228394328, 1.0912140118284737, 1.167769666187095, 1.2538380981220445, 1.3527034560492024, 1.4638659106412073, 1.5828878095865637, 1.7114832370000808, 1.855619862913596, 2.0167994608067406, 2.1923359933438635, 2.380539472943441, 2.5961585704688908, 2.832609932201364, 3.1067717682985085, 3.41536024365673, 3.757296537588393, 4.151294075870706, 4.623800085328394, 5.1880245271812, 5.872229391128905, 6.511612136647155, 7.209334588855921, 7.9411578658565665, 8.32439053442261, 8.333533286840078, 7.850300244107394, 7.153866241870963, 5.939108313352101, 4.915716881215529, 3.8024716071403644, 2.5716756890997305, 1.9346067828122504, 1.2037893092531886, 1.0711077409100167, 0.876040402775386, 0.7021847365830991, 0.6477445097703787, 0.709976050448786, 0.6503202844376943, 0.40395891837594655, 0.29921742438843163, 0.5151038019549756, 0.3972675999197689, 0.291323746379254, 0.9442625403627453, 1.6199681665327406, 0.1652763864386795, 0.17788087657296514, 1.143049228342116, 0.4337863670648724, 0.03891786739370852, 0.26158265768386724, 0.10008979571517725, 0.020063700919139622, 0.0021163801897082063};

  double puUL2018_up[79] = {
  4.427033518806137, 0.9469663121023734, 1.0174416155186763, 0.7567461352390532, 0.6605838665365286, 0.8754954005392594, 1.1313092673154128, 1.1326357875958253, 0.9294484701948171, 0.7588744922282916, 0.6724942604744212, 0.6433339039358077, 0.6300618927338424, 0.6410678183661892, 0.66177930918656, 0.6823178948259898, 0.6978641429015284, 0.7102507509207384, 0.7278805061457605, 0.7584185991562857, 0.7958841954126411, 0.8300380820515357, 0.86012353708099, 0.8863556624592162, 0.9013146396025089, 0.9056365628834131, 0.9037323188874081, 0.9073796282781231, 0.913370143051456, 0.9195274946165942, 0.9258927181806669, 0.9319248062338791, 0.937853489790987, 0.9457632536273032, 0.9556233084708337, 0.9688274085574717, 0.9859416689112538, 1.008659226631279, 1.036700312908097, 1.0728068648428424, 1.1168976811185884, 1.1687759737860204, 1.2295332608351925, 1.2994727374925614, 1.3751775396831496, 1.462315419580948, 1.5598808843652414, 1.6679223018701466, 1.7843951006001364, 1.900860691393007, 2.023911885581509, 2.1420273833258276, 2.2552885030180967, 2.3874138747974643, 2.4787636182617745, 2.5656966489160835, 2.6453657684827854, 2.771560372165124, 2.8805546587437396, 3.024404187765148, 3.1610718631332206, 3.242075267320954, 3.1878612783540587, 3.0743726265157227, 2.9981652982541176, 2.8564251423231033, 2.8371167190871667, 2.7235751248859748, 2.420398737577739, 2.455728408395543, 2.4652593823956077, 3.108093474932898, 3.2893619961858227, 2.6042678515582085, 2.0987904725266375, 2.3212413757359474, 2.5304042433660645, 2.681638418151081, 6.65397050302289};

  double puUL2018_nominal[79] = {
  4.759577811115876, 1.0806369717237092, 1.2167455803451304, 0.8809177232322252, 0.766238781602051, 1.0115455382170153, 1.3231440760320632, 1.3395604269689072, 1.10452553404012, 0.9123554695903464, 0.8240834618824157, 0.8003964951622832, 0.7907752910062616, 0.8067813395266399, 0.8323937633745241, 0.8564063860917435, 0.8725102728266475, 0.8821013625234374, 0.8946645337961082, 0.9187099917298068, 0.9464173719723038, 0.9664075022903863, 0.9801638231494445, 0.9908423882803207, 0.9925996984867392, 0.9873947618596791, 0.9797829612777218, 0.9812891367814947, 0.9868871679437331, 0.9928631365377237, 0.9982275877272523, 1.0017575672430654, 1.0033857910598627, 1.0051285022819616, 1.0066244072981032, 1.0088379403225771, 1.011660061007302, 1.0160315433489084, 1.0208793636980187, 1.028187369367983, 1.0371799969821327, 1.0471110279333733, 1.0584827432619959, 1.0710880521180892, 1.081836545461502, 1.0950999900345864, 1.1098211191190372, 1.1259872446384338, 1.1424750895564544, 1.1547481658546082, 1.1680747306007284, 1.1769617157833459, 1.1830875643510224, 1.1996388082203708, 1.1972249478862493, 1.1950813200622434, 1.1915770484702144, 1.2094746080085754, 1.2186050960721186, 1.2395588865807572, 1.252891945167981, 1.2392353337889774, 1.1711650424834192, 1.0816795882645718, 1.0067116658492365, 0.9124976805705236, 0.860095655162257, 0.7820992767128159, 0.6575846648861015, 0.6308822593112944, 0.59884727531515, 0.7141130200276866, 0.7151676386827616, 0.5360347845712561, 0.40905131887956614, 0.4283062945019823, 0.44173170946673673, 0.4423567008358185, 1.0353465278970846};

  double puUL2016postVFP_nominal[80] = {
  0.2777396890182089, 0.34160765222897554, 0.9147884372512897, 0.6969766985466789, 0.6331944809627448, 0.34199410096260385, 0.16008854559662297, 0.11065300316513929, 0.11101307459886778, 0.12984587110005172, 0.23169380388508315, 0.366612356685038, 0.48561422492768475, 0.5667111011782772, 0.6207905595577494, 0.6691239894113046, 0.7153514947652074, 0.7567679680738364, 0.7916065590899978, 0.8240581231636807, 0.8593328363067397, 0.9023513741403469, 0.9529888797866196, 1.007034405057875, 1.0610273210894379, 1.1189639109785383, 1.182069886080144, 1.251583802593513, 1.3272020394391935, 1.4061346042290674, 1.4829834345473947, 1.558630171974248, 1.6374796687891906, 1.7192023487130677, 1.7993247600393487, 1.8740826904900885, 1.9517062453987293, 2.02261116252284, 2.0939381681249896, 2.157717331743603, 2.2086499626036167, 2.2537198636928646, 2.3019837526669757, 2.353399130078361, 2.4136479861120086, 2.4142775200618, 2.403336918278076, 2.3761648304932756, 2.2362562110655073, 2.015779325415267, 1.7213829078058058, 1.439621449783133, 1.1190819149493005, 0.8937276592444401, 0.6945722519801218, 0.4944928862714944, 0.4085842677769634, 0.2863636854211633, 0.2870429783549122, 0.25879537364504734, 0.22131019809175634, 0.21077449219970423, 0.23219422545129315, 0.20962613291930407, 0.1266527268761778, 0.09046321462914171, 0.1493441030998368, 0.11006840469155137, 0.07696246990255044, 0.23752630161399235, 0.3876678376818466, 0.037606499178763346, 0.03847157851100001, 0.23493990354109198, 0.08472499008771356, 0.007222953159801814, 0.046131938667523305, 0.016772804914185292, 0.0030353647495220833, 0.00030416467025159223};

};

#endif
