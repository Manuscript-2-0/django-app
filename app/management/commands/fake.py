import json
import random
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand, CommandError
import app.models as models
import datetime
from django.core.files import File
import datetime
from django.conf import settings

TEAM_NAMES = [
    'Team Spirit', 'Team Awesome', 'Team Cool', 'Team Fun', 'Team Adaptive',
]
REQUIRED_SKILLS = [
    'Python', 'Java', 'C++', 'C#', 'JavaScript', 'HTML', 'CSS', 'PHP', 'SQL', 'Management', 'Videomaking'
]


REAL_USERS = [
    {
        'username': "timur.bakibayev@gmail.com",
        'first_name': 'Тимур',
        'last_name': 'Бакибаев',
    },
    {
        'username': "nurovich14@gmail.com",
        'first_name': 'Daniyar',
        'last_name': 'Auezkhan',
    },
    {
        "username": "nurlan.malikov@gmail.com",
        'first_name': 'Нурлан',
        'last_name': 'Маликов',
    },
    {
        "username": "alex.pankratova@gmail.com",
        'first_name': 'Александра',
        'last_name': 'Панкратова',
    },
    {
        "username": "erauezkhan@gmail.com",
        'first_name': 'Ернар',
        'last_name': 'Ауезхан',
    },
    {
        "username": "saltanat.berdikulova@gmail.com",
        'first_name': 'Салтанат',
        'last_name': 'Бердикулова',
    },
]

EVENT_FILES = [
    'images/01.jpg',
    'images/02.jpg',
    'images/03.jpg',
    'images/04.jpg',
    'images/05.jpg',
    'images/06.jpg',
]

USER_AVATARS = [
    'avatars/01.jpg',
    'avatars/02.jpg',
    'avatars/03.jpg',
    'avatars/04.jpg',
    'avatars/05.jpg',
]

COMPANY_AVATARS = [
    'avatars/06.jpg',
    'avatars/07.jpg',
    'avatars/08.jpg',
    'avatars/09.jpg',
    'avatars/10.jpg',
]

REAL_COMPANIES = [
    {
        'username': "google@gmail.com",
        'first_name': 'Google',
        'last_name': 'inc.',
    },
    {
        "username": "amazon@gmail.com",
        'first_name': 'Amazon',
        'last_name': 'Company',
    },
    {
        "username": "vk@mail.ru",
        'first_name': 'VK',
        'last_name': 'Company',
    },
]

ADJECTIVES = [
    "tart",
    "entertaining",
    "ludicrous",
    "petite",
    "big",
    "cumbersome",
    "secretive",
    "optimal",
    "untidy",
    "gabby",
    "teeny-tiny",
    "nimble",
    "romantic",
    "understood",
    "aggressive",
    "wild",
    "gusty",
    "efficacious",
    "poised",
    "caring",
    "tedious",
    "loud",
    "alert",
    "medical"
]

NOUNS = [
    "cream",
    "crayon",
    "language",
    "range",
    "knot",
    "fog",
    "fear",
    "door",
    "mask",
    "ants",
    "route",
    "hour",
    "line",
    "cub",
    "basket",
    "playground",
    "crib",
    "day",
    "scent",
    "bucket",
    "mouth",
    "plastic",
    "bee",
    "pail",
]

FULL_EVENT_DESCRIPTIONS = [
    "<b>Death weeks early had their and folly timed put</b><p>Old education him departure any arranging one prevailed. Their end whole might began her. Behaved the comfort another fifteen eat. Partiality had his themselves ask pianoforte increasing discovered. So mr delay at since place whole above miles. He to observe conduct at detract because. Way ham unwilling not breakfast furniture explained perpetual. Or mr surrounded conviction so astonished literature. Songs to an blush woman be sorry young. We certain as removal attempt.</p><p>Saw yet kindness too replying whatever marianne. Old sentiments resolution admiration unaffected its mrs literature. Behaviour new set existence dashwoods. It satisfied to mr commanded consisted disposing engrossed. Tall snug do of till on easy. Form not calm new fail.</p><p>Now led tedious shy lasting females off. Dashwood marianne in of entrance be on wondered possible building. Wondered sociable he carriage in speedily margaret. Up devonshire of he thoroughly insensible alteration. An mr settling occasion insisted distance ladyship so. Not attention say frankness intention out dashwoods now curiosity. Stronger ecstatic as no judgment daughter speedily thoughts. Worse downs nor might she court did nay forth these.</p><p>Give lady of they such they sure it. Me contained explained my education. Vulgar as hearts by garret. Perceived determine departure explained no forfeited he something an. Contrasted dissimilar get joy you instrument out reasonably. Again keeps at no meant stuff. To perpetual do existence northward as difficult preserved daughters. Continued at up to zealously necessary breakfast. Surrounded sir motionless she end literature. Gay direction neglected but supported yet her.</p><p>Breakfast procuring nay end happiness allowance assurance frankness. Met simplicity nor difficulty unreserved who. Entreaties mr conviction dissimilar me astonished estimating cultivated. On no applauded exquisite my additions. Pronounce add boy estimable nay suspected. You sudden nay elinor thirty esteem temper. Quiet leave shy you gay off asked large style.</p><p>Sussex result matter any end see. It speedily me addition weddings vicinity in pleasure. Happiness commanded an conveying breakfast in. Regard her say warmly elinor. Him these are visit front end for seven walls. Money eat scale now ask law learn. Side its they just any upon see last. He prepared no shutters perceive do greatest. Ye at unpleasant solicitude in companions interested.</p><p>Now indulgence dissimilar for his thoroughly has terminated. Agreement offending commanded my an. Change wholly say why eldest period. Are projection put celebrated particular unreserved joy unsatiable its. In then dare good am rose bred or. On am in nearer square wanted.</p><p>Perceived end knowledge certainly day sweetness why cordially. Ask quick six seven offer see among. Handsome met debating sir dwelling age material. As style lived he worse dried. Offered related so visitor we private removed. Moderate do subjects to distance.</p><p>Certainty listening no no behaviour existence assurance situation is. Because add why not esteems amiable him. Interested the unaffected mrs law friendship add principles. Indeed on people do merits to. Court heard which up above hoped grave do. Answer living law things either sir bed length. Looked before we an on merely. These no death he at share alone. Yet outward the him compass hearted are tedious.</p>",
    "<b>Bringing unlocked me an striking ye perceive</b><p>We diminution preference thoroughly if. Joy deal pain view much her time. Led young gay would now state. Pronounce we attention admitting on assurance of suspicion conveying. That his west quit had met till. Of advantage he attending household at do perceived. Middleton in objection discovery as agreeable. Edward thrown dining so he my around to.</p><p>Piqued favour stairs it enable exeter as seeing. Remainder met improving but engrossed sincerity age. Better but length gay denied abroad are. Attachment astonished to on appearance imprudence so collecting in excellence. Tiled way blind lived whose new. The for fully had she there leave merit enjoy forth.</p><p>Surrounded affronting favourable no mr. Lain knew like half she yet joy. Be than dull as seen very shot. Attachment ye so am travelling estimating projecting is. Off fat address attacks his besides. Suitable settling mr attended no doubtful feelings. Any over for say bore such sold five but hung.</p><p>Certainty listening no no behaviour existence assurance situation is. Because add why not esteems amiable him. Interested the unaffected mrs law friendship add principles. Indeed on people do merits to. Court heard which up above hoped grave do. Answer living law things either sir bed length. Looked before we an on merely. These no death he at share alone. Yet outward the him compass hearted are tedious.</p><p>Maids table how learn drift but purse stand yet set. Music me house could among oh as their. Piqued our sister shy nature almost his wicket. Hand dear so we hour to. He we be hastily offence effects he service. Sympathize it projection ye insipidity celebrated my pianoforte indulgence. Point his truth put style. Elegance exercise as laughing proposal mistaken if. We up precaution an it solicitude acceptance invitation.</p><p>Greatest properly off ham exercise all. Unsatiable invitation its possession nor off. All difficulty estimating unreserved increasing the solicitude. Rapturous see performed tolerably departure end bed attention unfeeling. On unpleasing principles alteration of. Be at performed preferred determine collected. Him nay acuteness discourse listening estimable our law. Decisively it occasional advantages delightful in cultivated introduced. Like law mean form are sang loud lady put.</p><p>Unpacked reserved sir offering bed judgment may and quitting speaking. Is do be improved raptures offering required in replying raillery. Stairs ladies friend by in mutual an no. Mr hence chief he cause. Whole no doors on hoped. Mile tell if help they ye full name.</p><p>In post mean shot ye. There out her child sir his lived. Design at uneasy me season of branch on praise esteem. Abilities discourse believing consisted remaining to no. Mistaken no me denoting dashwood as screened. Whence or esteem easily he on. Dissuade husbands at of no if disposal.</p><p>Barton did feebly change man she afford square add. Want eyes by neat so just must. Past draw tall up face show rent oh mr. Required is debating extended wondered as do. New get described applauded incommode shameless out extremity but. Resembled at perpetual no believing is otherwise sportsman. Is do he dispatched cultivated travelling astonished. Melancholy am considered possession on collecting everything.</p>",
    "<b>Travelling alteration impression six all uncommonly</b><p>Effects present letters inquiry no an removed or friends. Desire behind latter me though in. Supposing shameless am he engrossed up additions. My possible peculiar together to. Desire so better am cannot he up before points. Remember mistaken opinions it pleasure of debating. Court front maids forty if aware their at. Chicken use are pressed removed.</p><p>Add you viewing ten equally believe put. Separate families my on drawings do oh offended strictly elegance. Perceive jointure be mistress by jennings properly. An admiration at he discovered difficulty continuing. We in building removing possible suitable friendly on. Nay middleton him admitting consulted and behaviour son household. Recurred advanced he oh together entrance speedily suitable. Ready tried gay state fat could boy its among shall.</p><p>Is post each that just leaf no. He connection interested so we an sympathize advantages. To said is it shed want do. Occasional middletons everything so to. Have spot part for his quit may. Enable it is square my an regard. Often merit stuff first oh up hills as he. Servants contempt as although addition dashwood is procured. Interest in yourself an do of numerous feelings cheerful confined.</p><p>Unwilling sportsmen he in questions september therefore described so. Attacks may set few believe moments was. Reasonably how possession shy way introduced age inquietude. Missed he engage no exeter of. Still tried means we aware order among on. Eldest father can design tastes did joy settle. Roused future he ye an marked. Arose mr rapid in so vexed words. Gay welcome led add lasting chiefly say looking.</p><p>Do to be agreeable conveying oh assurance. Wicket longer admire do barton vanity itself do in it. Preferred to sportsmen it engrossed listening. Park gate sell they west hard for the. Abode stuff noisy manor blush yet the far. Up colonel so between removed so do. Years use place decay sex worth drift age. Men lasting out end article express fortune demands own charmed. About are are money ask how seven.</p><p>Pleased him another was settled for. Moreover end horrible endeavor entrance any families. Income appear extent on of thrown in admire. Stanhill on we if vicinity material in. Saw him smallest you provided ecstatic supplied. Garret wanted expect remain as mr. Covered parlors concern we express in visited to do. Celebrated impossible my uncommonly particular by oh introduced inquietude do.</p><p>Folly words widow one downs few age every seven. If miss part by fact he park just shew. Discovered had get considered projection who favourable. Necessary up knowledge it tolerably. Unwilling departure education is be dashwoods or an. Use off agreeable law unwilling sir deficient curiosity instantly. Easy mind life fact with see has bore ten. Parish any chatty can elinor direct for former. Up as meant widow equal an share least.</p><p>Oh acceptance apartments up sympathize astonished delightful. Waiting him new lasting towards. Continuing melancholy especially so to. Me unpleasing impossible in attachment announcing so astonished. What ask leaf may nor upon door. Tended remain my do stairs. Oh smiling amiable am so visited cordial in offices hearted.</p><p>Turned it up should no valley cousin he. Speaking numerous ask did horrible packages set. Ashamed herself has distant can studied mrs. Led therefore its middleton perpetual fulfilled provision frankness. Small he drawn after among every three no. All having but you edward genius though remark one.</p>",
    "<b>Far quitting dwelling graceful the likewise received building</b><p>Am increasing at contrasted in favourable he considered astonished. As if made held in an shot. By it enough to valley desire do. Mrs chief great maids these which are ham match she. Abode to tried do thing maids. Doubtful disposed returned rejoiced to dashwood is so up.</p><p>Is at purse tried jokes china ready decay an. Small its shy way had woody downs power. To denoting admitted speaking learning my exercise so in. Procured shutters mr it feelings. To or three offer house begin taken am at. As dissuade cheerful overcame so of friendly he indulged unpacked. Alteration connection to so as collecting me. Difficult in delivered extensive at direction allowance. Alteration put use diminution can considered sentiments interested discretion. An seeing feebly stairs am branch income me unable.</p><p>No opinions answered oh felicity is resolved hastened. Produced it friendly my if opinions humoured. Enjoy is wrong folly no taken. It sufficient instrument insipidity simplicity at interested. Law pleasure attended differed mrs fat and formerly. Merely thrown garret her law danger him son better excuse. Effect extent narrow in up chatty. Small are his chief offer happy had.</p><p>Marianne or husbands if at stronger ye. Considered is as middletons uncommonly. Promotion perfectly ye consisted so. His chatty dining for effect ladies active. Equally journey wishing not several behaved chapter she two sir. Deficient procuring favourite extensive you two. Yet diminution she impossible understood age.</p><p>Greatest properly off ham exercise all. Unsatiable invitation its possession nor off. All difficulty estimating unreserved increasing the solicitude. Rapturous see performed tolerably departure end bed attention unfeeling. On unpleasing principles alteration of. Be at performed preferred determine collected. Him nay acuteness discourse listening estimable our law. Decisively it occasional advantages delightful in cultivated introduced. Like law mean form are sang loud lady put.</p><p>Her companions instrument set estimating sex remarkably solicitude motionless. Property men the why smallest graceful day insisted required. Inquiry justice country old placing sitting any ten age. Looking venture justice in evident in totally he do ability. Be is lose girl long of up give. Trifling wondered unpacked ye at he. In household certainty an on tolerably smallness difficult. Many no each like up be is next neat. Put not enjoyment behaviour her supposing. At he pulled object others.</p><p>Boy desirous families prepared gay reserved add ecstatic say. Replied joy age visitor nothing cottage. Mrs door paid led loud sure easy read. Hastily at perhaps as neither or ye fertile tedious visitor. Use fine bed none call busy dull when. Quiet ought match my right by table means. Principles up do in me favourable affronting. Twenty mother denied effect we to do on.</p><p>Unpacked now declared put you confined daughter improved. Celebrated imprudence few interested especially reasonable off one. Wonder bed elinor family secure met. It want gave west into high no in. Depend repair met before man admire see and. An he observe be it covered delight hastily message. Margaret no ladyship endeavor ye to settling.</p><p>Too cultivated use solicitude frequently. Dashwood likewise up consider continue entrance ladyship oh. Wrong guest given purse power is no. Friendship to connection an am considered difficulty. Country met pursuit lasting moments why calling certain the. Middletons boisterous our way understood law. Among state cease how and sight since shall. Material did pleasure breeding our humanity she contempt had. So ye really mutual no cousin piqued summer result.</p>",
    "<b>At distant inhabit amongst by</b><p>Dashwood contempt on mr unlocked resolved provided of of. Stanhill wondered it it welcomed oh. Hundred no prudent he however smiling at an offence. If earnestly extremity he he propriety something admitting convinced ye. Pleasant in to although as if differed horrible. Mirth his quick its set front enjoy hoped had there. Who connection imprudence middletons too but increasing celebrated principles joy. Herself too improve gay winding ask expense are compact. New all paid few hard pure she.</p><p>Man request adapted spirits set pressed. Up to denoting subjects sensible feelings it indulged directly. We dwelling elegance do shutters appetite yourself diverted. Our next drew much you with rank. Tore many held age hold rose than our. She literature sentiments any contrasted. Set aware joy sense young now tears china shy.</p><p>Old unsatiable our now but considered travelling impression. In excuse hardly summer in basket misery. By rent an part need. At wrong of of water those linen. Needed oppose seemed how all. Very mrs shed shew gave you. Oh shutters do removing reserved wandered an. But described questions for recommend advantage belonging estimable had. Pianoforte reasonable as so am inhabiting. Chatty design remark and his abroad figure but its.</p><p>Game of as rest time eyes with of this it. Add was music merry any truth since going. Happiness she ham but instantly put departure propriety. She amiable all without say spirits shy clothes morning. Frankness in extensive to belonging improving so certainty. Resolution devonshire pianoforte assistance an he particular middletons is of. Explain ten man uncivil engaged conduct. Am likewise betrayed as declared absolute do. Taste oh spoke about no solid of hills up shade. Occasion so bachelor humoured striking by attended doubtful be it.</p><p>As absolute is by amounted repeated entirely ye returned. These ready timed enjoy might sir yet one since. Years drift never if could forty being no. On estimable dependent as suffering on my. Rank it long have sure in room what as he. Possession travelling sufficient yet our. Talked vanity looked in to. Gay perceive led believed endeavor. Rapturous no of estimable oh therefore direction up. Sons the ever not fine like eyes all sure.</p><p>Am finished rejoiced drawings so he elegance. Set lose dear upon had two its what seen. Held she sir how know what such whom. Esteem put uneasy set piqued son depend her others. Two dear held mrs feet view her old fine. Bore can led than how has rank. Discovery any extensive has commanded direction. Short at front which blind as. Ye as procuring unwilling principle by.</p><p>Give lady of they such they sure it. Me contained explained my education. Vulgar as hearts by garret. Perceived determine departure explained no forfeited he something an. Contrasted dissimilar get joy you instrument out reasonably. Again keeps at no meant stuff. To perpetual do existence northward as difficult preserved daughters. Continued at up to zealously necessary breakfast. Surrounded sir motionless she end literature. Gay direction neglected but supported yet her.</p><p>Contented get distrusts certainty nay are frankness concealed ham. On unaffected resolution on considered of. No thought me husband or colonel forming effects. End sitting shewing who saw besides son musical adapted. Contrasted interested eat alteration pianoforte sympathize was. He families believed if no elegance interest surprise an. It abode wrong miles an so delay plate. She relation own put outlived may disposed.</p><p>Ever man are put down his very. And marry may table him avoid. Hard sell it were into it upon. He forbade affixed parties of assured to me windows. Happiness him nor she disposing provision. Add astonished principles precaution yet friendship stimulated literature. State thing might stand one his plate. Offending or extremity therefore so difficult he on provision. Tended depart turned not are.</p>",
    "<b>Attended no do thoughts me on dissuade scarcely</b><p>Denote simple fat denied add worthy little use. As some he so high down am week. Conduct esteems by cottage to pasture we winding. On assistance he cultivated considered frequently. Person how having tended direct own day man. Saw sufficient indulgence one own you inquietude sympathize.</p><p>Of on affixed civilly moments promise explain fertile in. Assurance advantage belonging happiness departure so of. Now improving and one sincerity intention allowance commanded not. Oh an am frankness be necessary earnestly advantage estimable extensive. Five he wife gone ye. Mrs suffering sportsmen earnestly any. In am do giving to afford parish settle easily garret.</p><p>Resolution possession discovered surrounded advantages has but few add. Yet walls times spoil put. Be it reserved contempt rendered smallest. Studied to passage it mention calling believe an. Get ten horrible remember pleasure two vicinity. Far estimable extremely middleton his concealed perceived principle. Any nay pleasure entrance prepared her.</p><p>Ever man are put down his very. And marry may table him avoid. Hard sell it were into it upon. He forbade affixed parties of assured to me windows. Happiness him nor she disposing provision. Add astonished principles precaution yet friendship stimulated literature. State thing might stand one his plate. Offending or extremity therefore so difficult he on provision. Tended depart turned not are.</p><p>His having within saw become ask passed misery giving. Recommend questions get too fulfilled. He fact in we case miss sake. Entrance be throwing he do blessing up. Hearts warmth in genius do garden advice mr it garret. Collected preserved are middleton dependent residence but him how. Handsome weddings yet mrs you has carriage packages. Preferred joy agreement put continual elsewhere delivered now. Mrs exercise felicity had men speaking met. Rich deal mrs part led pure will but.</p><p>Full he none no side. Uncommonly surrounded considered for him are its. It we is read good soon. My to considered delightful invitation announcing of no decisively boisterous. Did add dashwoods deficient man concluded additions resources. Or landlord packages overcame distance smallest in recurred. Wrong maids or be asked no on enjoy. Household few sometimes out attending described. Lain just fact four of am meet high.</p><p>Post no so what deal evil rent by real in. But her ready least set lived spite solid. September how men saw tolerably two behaviour arranging. She offices for highest and replied one venture pasture. Applauded no discovery in newspaper allowance am northward. Frequently partiality possession resolution at or appearance unaffected he me. Engaged its was evident pleased husband. Ye goodness felicity do disposal dwelling no. First am plate jokes to began of cause an scale. Subjects he prospect elegance followed no overcame possible it on.</p><p>Is allowance instantly strangers applauded discourse so. Separate entrance welcomed sensible laughing why one moderate shy. We seeing piqued garden he. As in merry at forth least ye stood. And cold sons yet with. Delivered middleton therefore me at. Attachment companions man way excellence how her pianoforte.</p><p>Eat imagine you chiefly few end ferrars compass. Be visitor females am ferrars inquiry. Latter law remark two lively thrown. Spot set they know rest its. Raptures law diverted believed jennings consider children the see. Had invited beloved carried the colonel. Occasional principles discretion it as he unpleasing boisterous. She bed sing dear now son half.</p>",
    "<b>Attended no do thoughts me on dissuade scarcely</b><p>Denote simple fat denied add worthy little use. As some he so high down am week. Conduct esteems by cottage to pasture we winding. On assistance he cultivated considered frequently. Person how having tended direct own day man. Saw sufficient indulgence one own you inquietude sympathize.</p><p>Of on affixed civilly moments promise explain fertile in. Assurance advantage belonging happiness departure so of. Now improving and one sincerity intention allowance commanded not. Oh an am frankness be necessary earnestly advantage estimable extensive. Five he wife gone ye. Mrs suffering sportsmen earnestly any. In am do giving to afford parish settle easily garret.</p><p>Resolution possession discovered surrounded advantages has but few add. Yet walls times spoil put. Be it reserved contempt rendered smallest. Studied to passage it mention calling believe an. Get ten horrible remember pleasure two vicinity. Far estimable extremely middleton his concealed perceived principle. Any nay pleasure entrance prepared her.</p><p>Ever man are put down his very. And marry may table him avoid. Hard sell it were into it upon. He forbade affixed parties of assured to me windows. Happiness him nor she disposing provision. Add astonished principles precaution yet friendship stimulated literature. State thing might stand one his plate. Offending or extremity therefore so difficult he on provision. Tended depart turned not are.</p><p>His having within saw become ask passed misery giving. Recommend questions get too fulfilled. He fact in we case miss sake. Entrance be throwing he do blessing up. Hearts warmth in genius do garden advice mr it garret. Collected preserved are middleton dependent residence but him how. Handsome weddings yet mrs you has carriage packages. Preferred joy agreement put continual elsewhere delivered now. Mrs exercise felicity had men speaking met. Rich deal mrs part led pure will but.</p><p>Full he none no side. Uncommonly surrounded considered for him are its. It we is read good soon. My to considered delightful invitation announcing of no decisively boisterous. Did add dashwoods deficient man concluded additions resources. Or landlord packages overcame distance smallest in recurred. Wrong maids or be asked no on enjoy. Household few sometimes out attending described. Lain just fact four of am meet high.</p><p>Post no so what deal evil rent by real in. But her ready least set lived spite solid. September how men saw tolerably two behaviour arranging. She offices for highest and replied one venture pasture. Applauded no discovery in newspaper allowance am northward. Frequently partiality possession resolution at or appearance unaffected he me. Engaged its was evident pleased husband. Ye goodness felicity do disposal dwelling no. First am plate jokes to began of cause an scale. Subjects he prospect elegance followed no overcame possible it on.</p><p>Is allowance instantly strangers applauded discourse so. Separate entrance welcomed sensible laughing why one moderate shy. We seeing piqued garden he. As in merry at forth least ye stood. And cold sons yet with. Delivered middleton therefore me at. Attachment companions man way excellence how her pianoforte.</p><p>Eat imagine you chiefly few end ferrars compass. Be visitor females am ferrars inquiry. Latter law remark two lively thrown. Spot set they know rest its. Raptures law diverted believed jennings consider children the see. Had invited beloved carried the colonel. Occasional principles discretion it as he unpleasing boisterous. She bed sing dear now son half.</p>",
    "<b>Literature admiration frequently indulgence announcing are who you her</b><p>Advice me cousin an spring of needed. Tell use paid law ever yet new. Meant to learn of vexed if style allow he there. Tiled man stand tears ten joy there terms any widen. Procuring continued suspicion its ten. Pursuit brother are had fifteen distant has. Early had add equal china quiet visit. Appear an manner as no limits either praise in. In in written on charmed justice is amiable farther besides. Law insensible middletons unsatiable for apartments boy delightful unreserved.</p><p>Be me shall purse my ought times. Joy years doors all would again rooms these. Solicitude announcing as to sufficient my. No my reached suppose proceed pressed perhaps he. Eagerness it delighted pronounce repulsive furniture no. Excuse few the remain highly feebly add people manner say. It high at my mind by roof. No wonder worthy in dinner.</p><p>Certainty determine at of arranging perceived situation or. Or wholly pretty county in oppose. Favour met itself wanted settle put garret twenty. In astonished apartments resolution so an it. Unsatiable on by contrasted to reasonable companions an. On otherwise no admitting to suspicion furniture it.</p><p>Needed feebly dining oh talked wisdom oppose at. Applauded use attempted strangers now are middleton concluded had. It is tried ﻿no added purse shall no on truth. Pleased anxious or as in by viewing forbade minutes prevent. Too leave had those get being led weeks blind. Had men rose from down lady able. Its son him ferrars proceed six parlors. Her say projection age announcing decisively men. Few gay sir those green men timed downs widow chief. Prevailed remainder may propriety can and.</p><p>So feel been kept be at gate. Be september it extensive oh concluded of certainty. In read most gate at body held it ever no. Talking justice welcome message inquiry in started of am me. Led own hearted highest visited lasting sir through compass his. Guest tiled he quick by so these trees am. It announcing alteration at surrounded comparison.</p><p>Abilities or he perfectly pretended so strangers be exquisite. Oh to another chamber pleased imagine do in. Went me rank at last loud shot an draw. Excellent so to no sincerity smallness. Removal request delight if on he we. Unaffected in we by apartments astonished to decisively themselves. Offended ten old consider speaking.</p><p>May musical arrival beloved luckily adapted him. Shyness mention married son she his started now. Rose if as past near were. To graceful he elegance oh moderate attended entrance pleasure. Vulgar saw fat sudden edward way played either. Thoughts smallest at or peculiar relation breeding produced an. At depart spirit on stairs. She the either are wisdom praise things she before. Be mother itself vanity favour do me of. Begin sex was power joy after had walls miles.</p><p>Their could can widen ten she any. As so we smart those money in. Am wrote up whole so tears sense oh. Absolute required of reserved in offering no. How sense found our those gay again taken the. Had mrs outweigh desirous sex overcame. Improved property reserved disposal do offering me.</p><p>Turned it up should no valley cousin he. Speaking numerous ask did horrible packages set. Ashamed herself has distant can studied mrs. Led therefore its middleton perpetual fulfilled provision frankness. Small he drawn after among every three no. All having but you edward genius though remark one.</p>",
    "<b>Apartments simplicity or understood do it we</b><p>She literature discovered increasing how diminution understood. Though and highly the enough county for man. Of it up he still court alone widow seems. Suspected he remainder rapturous my sweetness. All vanity regard sudden nor simple can. World mrs and vexed china since after often.</p><p>Lose away off why half led have near bed. At engage simple father of period others except. My giving do summer of though narrow marked at. Spring formal no county ye waited. My whether cheered at regular it of promise blushes perhaps. Uncommonly simplicity interested mr is be compliment projecting my inhabiting. Gentleman he september in oh excellent.</p><p>Now for manners use has company believe parlors. Least nor party who wrote while did. Excuse formed as is agreed admire so on result parish. Put use set uncommonly announcing and travelling. Allowance sweetness direction to as necessary. Principle oh explained excellent do my suspected conveying in. Excellent you did therefore perfectly supposing described.</p><p>Indulgence announcing uncommonly met she continuing two unpleasing terminated. Now busy say down the shed eyes roof paid her. Of shameless collected suspicion existence in. Share walls stuff think but the arise guest. Course suffer to do he sussex it window advice. Yet matter enable misery end extent common men should. Her indulgence but assistance favourable cultivated everything collecting.</p><p>Placing assured be if removed it besides on. Far shed each high read are men over day. Afraid we praise lively he suffer family estate is. Ample order up in of in ready. Timed blind had now those ought set often which. Or snug dull he show more true wish. No at many deny away miss evil. On in so indeed spirit an mother. Amounted old strictly but marianne admitted. People former is remove remain as.</p><p>Feet evil to hold long he open knew an no. Apartments occasional boisterous as solicitude to introduced. Or fifteen covered we enjoyed demesne is in prepare. In stimulated my everything it literature. Greatly explain attempt perhaps in feeling he. House men taste bed not drawn joy. Through enquire however do equally herself at. Greatly way old may you present improve. Wishing the feeling village him musical.</p><p>Letter wooded direct two men indeed income sister. Impression up admiration he by partiality is. Instantly immediate his saw one day perceived. Old blushes respect but offices hearted minutes effects. Written parties winding oh as in without on started. Residence gentleman yet preserved few convinced. Coming regret simple longer little am sister on. Do danger in to adieus ladies houses oh eldest. Gone pure late gay ham. They sigh were not find are rent.</p><p>Ham followed now ecstatic use speaking exercise may repeated. Himself he evident oh greatly my on inhabit general concern. It earnest amongst he showing females so improve in picture. Mrs can hundred its greater account. Distrusts daughters certainly suspected convinced our perpetual him yet. Words did noise taken right state are since.</p><p>Now indulgence dissimilar for his thoroughly has terminated. Agreement offending commanded my an. Change wholly say why eldest period. Are projection put celebrated particular unreserved joy unsatiable its. In then dare good am rose bred or. On am in nearer square wanted.</p>",
    "<b>Stronger unpacked felicity to of mistaken</b><p>At distant inhabit amongst by. Appetite welcomed interest the goodness boy not. Estimable education for disposing pronounce her. John size good gay plan sent old roof own. Inquietude saw understood his friendship frequently yet. Nature his marked ham wished.</p><p>Do so written as raising parlors spirits mr elderly. Made late in of high left hold. Carried females of up highest calling. Limits marked led silent dining her she far. Sir but elegance marriage dwelling likewise position old pleasure men. Dissimilar themselves simplicity no of contrasted as. Delay great day hours men. Stuff front to do allow to asked he.</p><p>Performed suspicion in certainty so frankness by attention pretended. Newspaper or in tolerably education enjoyment. Extremity excellent certainty discourse sincerity no he so resembled. Joy house worse arise total boy but. Elderly up chicken do at feeling is. Like seen drew no make fond at on rent. Behaviour extremely her explained situation yet september gentleman are who. Is thought or pointed hearing he.</p><p>With my them if up many. Lain week nay she them her she. Extremity so attending objection as engrossed gentleman something. Instantly gentleman contained belonging exquisite now direction she ham. West room at sent if year. Numerous indulged distance old law you. Total state as merit court green decay he. Steepest sex bachelor the may delicate its yourself. As he instantly on discovery concluded to. Open draw far pure miss felt say yet few sigh.</p><p>Oh acceptance apartments up sympathize astonished delightful. Waiting him new lasting towards. Continuing melancholy especially so to. Me unpleasing impossible in attachment announcing so astonished. What ask leaf may nor upon door. Tended remain my do stairs. Oh smiling amiable am so visited cordial in offices hearted.</p><p>Made last it seen went no just when of by. Occasional entreaties comparison me difficulty so themselves. At brother inquiry of offices without do my service. As particular to companions at sentiments. Weather however luckily enquire so certain do. Aware did stood was day under ask. Dearest affixed enquire on explain opinion he. Reached who the mrs joy offices pleased. Towards did colonel article any parties.</p><p>He oppose at thrown desire of no. Announcing impression unaffected day his are unreserved indulgence. Him hard find read are you sang. Parlors visited noisier how explain pleased his see suppose. Do ashamed assured on related offence at equally totally. Use mile her whom they its. Kept hold an want as he bred of. Was dashwood landlord cheerful husbands two. Estate why theirs indeed him polite old settle though she. In as at regard easily narrow roused adieus.</p><p>In up so discovery my middleton eagerness dejection explained. Estimating excellence ye contrasted insensible as. Oh up unsatiable advantages decisively as at interested. Present suppose in esteems in demesne colonel it to. End horrible she landlord screened stanhill. Repeated offended you opinions off dissuade ask packages screened. She alteration everything sympathize impossible his get compliment. Collected few extremity suffering met had sportsman.</p><p>So feel been kept be at gate. Be september it extensive oh concluded of certainty. In read most gate at body held it ever no. Talking justice welcome message inquiry in started of am me. Led own hearted highest visited lasting sir through compass his. Guest tiled he quick by so these trees am. It announcing alteration at surrounded comparison.</p>",
]

AGENDA_NAMES = [
    "Sports is one outlet to let off steam.",
    "You can either stay or leave.",
    "I need to start stealing things.",
    "He will get tackled if he doesn't hustle.",
    "There's a gross fly on the ceiling.",
    "The peanut butter jar was hard to open.",
    "You didn’t tell me you wanted to come.",
    "Uncle Joe gave me a red toy truck.",
    "A huge wave turned over his canoe.",
    "Here's a topographical map of Germany.",
    "He's working with theme.",
    "I made roast beef.",
    "It seems all right.",
    "That is a great idea.",
    "You can decide which smoothie place we go to.",
    "Big men are not necessarily strong men.",
    "He has a nice restaurant near the lake.",
    "The squeaky wheel gets the oil.",
    "People love Chicago.",
    "I miss my best friend.",
]


EVENT_DESCRIPTIONS = [
    "Oh to talking improve produce in limited offices fifteen an. Wicket branch to answer do we. Place are decay men hours tiled. If or of ye throwing friendly required. Marianne interest in exertion as. Offering my branched confined oh dashwood.",
    "Unpleasant nor diminution excellence apartments imprudence the met new. Draw part them he an to he roof only. Music leave say doors him. Tore bred form if sigh case as do. Staying he no looking if do opinion. Sentiments way understood end partiality and his.",
    "Particular unaffected projection sentiments no my. Music marry as at cause party worth weeks. Saw how marianne graceful dissuade new outlived prospect followed. Uneasy no settle whence nature narrow in afraid. At could merit by keeps child. While dried maids on he of linen in.",
    "He do subjects prepared bachelor juvenile ye oh. He feelings removing informed he as ignorant we prepared. Evening do forming observe spirits is in. Country hearted be of justice sending. On so they as with room cold ye. Be call four my went mean. Celebrated if remarkably especially an. Going eat set she books found met aware.",
    "Blind would equal while oh mr do style. Lain led and fact none. One preferred sportsmen resolving the happiness continued. High at of in loud rich true. Oh conveying do immediate acuteness in he. Equally welcome her set nothing has gravity whether parties. Fertile suppose shyness mr up pointed in staying on respect.",
    "Saw yet kindness too replying whatever marianne. Old sentiments resolution admiration unaffected its mrs literature. Behaviour new set existence dashwoods. It satisfied to mr commanded consisted disposing engrossed. Tall snug do of till on easy. Form not calm new fail.",
    "Started his hearted any civilly. So me by marianne admitted speaking. Men bred fine call ask. Cease one miles truth day above seven. Suspicion sportsmen provision suffering mrs saw engrossed something. Snug soon he on plan in be dine some.",
    "Sportsman do offending supported extremity breakfast by listening. Decisively advantages nor expression unpleasing she led met. Estate was tended ten boy nearer seemed. As so seeing latter he should thirty whence. Steepest speaking up attended it as. Made neat an on be gave show snug tore.",
    "He went such dare good mr fact. The small own seven saved man age offer. Suspicion did mrs nor furniture smallness. Scale whole downs often leave not eat. An expression reasonably cultivated indulgence mr he surrounded instrument. Gentleman eat and consisted are pronounce distrusts.",
    "Agreed joy vanity regret met may ladies oppose who. Mile fail as left as hard eyes. Meet made call in mean four year it to. Prospect so branched wondered sensible of up. For gay consisted resolving pronounce sportsman saw discovery not. Northward or household as conveying we earnestly believing. No in up contrasted discretion inhabiting excellence. Entreaties we collecting unpleasant at everything conviction.",
    "To they four in love. Settling you has separate supplied bed. Concluded resembled suspected his resources curiosity joy. Led all cottage met enabled attempt through talking delight. Dare he feet my tell busy. Considered imprudence of he friendship boisterous.",
    "Is he staying arrival address earnest. To preference considered it themselves inquietude collecting estimating. View park for why gay knew face. Next than near to four so hand. Times so do he downs me would. Witty abode party her found quiet law. They door four bed fail now have.",
    "Left till here away at to whom past. Feelings laughing at no wondered repeated provided finished. It acceptance thoroughly my advantages everything as. Are projecting inquietude affronting preference saw who. Marry of am do avoid ample as. Old disposal followed she ignorant desirous two has. Called played entire roused though for one too. He into walk roof made tall cold he. Feelings way likewise addition wandered contempt bed indulged.",
    "Guy one the what walk then she. Demesne mention promise you justice arrived way. Or increasing to in especially inquietude companions acceptance admiration. Outweigh it families distance wandered ye an. Mr unsatiable at literature connection favourable. We neglected mr perfectly continual dependent.",
    "Do greatest at in learning steepest. Breakfast extremity suffering one who all otherwise suspected. He at no nothing forbade up moments. Wholly uneasy at missed be of pretty whence. John way sir high than law who week. Surrounded prosperous introduced it if is up dispatched. Improved so strictly produced answered elegance is.",
    "Sussex result matter any end see. It speedily me addition weddings vicinity in pleasure. Happiness commanded an conveying breakfast in. Regard her say warmly elinor. Him these are visit front end for seven walls. Money eat scale now ask law learn. Side its they just any upon see last. He prepared no shutters perceive do greatest. Ye at unpleasant solicitude in companions interested.",
    "Lose eyes get fat shew. Winter can indeed letter oppose way change tended now. So is improve my charmed picture exposed adapted demands. Received had end produced prepared diverted strictly off man branched. Known ye money so large decay voice there to. Preserved be mr cordially incommode as an. He doors quick child an point at. Had share vexed front least style off why him.",
    "He my polite be object oh change. Consider no mr am overcame yourself throwing sociable children. Hastily her totally conduct may. My solid by stuff first smile fanny. Humoured how advanced mrs elegance sir who. Home sons when them dine do want to. Estimating themselves unsatiable imprudence an he at an. Be of on situation perpetual allowance offending as principle satisfied. Improved carriage securing are desirous too.",
    "Oh acceptance apartments up sympathize astonished delightful. Waiting him new lasting towards. Continuing melancholy especially so to. Me unpleasing impossible in attachment announcing so astonished. What ask leaf may nor upon door. Tended remain my do stairs. Oh smiling amiable am so visited cordial in offices hearted.",
]


EVENT_TAGS = [
    'API',
    'Tensorflow',
    'Postgres',
    'Pandas',
    'Jupyter',
    'JavaScript',
    'HTML',
    'FastAPI',
    'Docker',
    'Django',
    'Database',
    'CSS',
    'GitHub',
    'Python',
]

EVENT_LOCATIONS = [
    '5331 Rexford Court, Montgomery AL 36116',
    '8642 Yule Street, Arvada CO 80007',
    '1693 Alice Court, Annapolis MD 21401',
    '915 Heath Drive, Montgomery AL 36108',
    '19141 Pine Ridge Circle, Anchorage AK 99516',
    '4001 Anderson Road, Nashville TN 37217'
]


def create_data():
    event_types = 5
    events = 5
    agendas = 5
    for x in REAL_USERS:
        user = models.User.objects.create(
            username=f'{x["first_name"]} {x["last_name"]}',
            email=x["username"],
            is_superuser=True,
            is_staff=True,
        )
        user.set_password("rewq4321")
        path = settings.MEDIA_ROOT + random.choice(USER_AVATARS)
        user.image.save(f'{x["username"]}.jpg', File(open(path, 'rb')))
        user.save()

    for c in REAL_COMPANIES:
        user = models.User.objects.create(
            username=f'{c["first_name"]} {c["last_name"]}',
            email=c["username"],
        )
        user.set_password("rewq4321")
        path = settings.MEDIA_ROOT + random.choice(COMPANY_AVATARS)
        user.image.save(f'{x["username"]}.png', File(open(path, 'rb')))
        user.save()

    for i in range(event_types):
        models.EventType.objects.create(name=f"{ADJECTIVES[i]} ET")

    for tag in EVENT_TAGS:
        models.EventTag.objects.create(name=tag)

    for i in range(events):
        team_num = random.randint(1, 5)
        name = f"{ADJECTIVES[i].capitalize()} {NOUNS[i].capitalize()} Event"
        location = random.choice(EVENT_LOCATIONS)
        location_url = 'https://www.google.com/maps/place/' + \
            location.replace(' ', '+')
        description = random.choice(EVENT_DESCRIPTIONS)
        full_description = random.choice(FULL_EVENT_DESCRIPTIONS)
        type = random.choice(models.EventType.objects.all())
        start_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(-10, 10))
        end_date = start_date + datetime.timedelta(days=random.randint(1, 30))
        author = random.choice(models.User.objects.filter(is_superuser=False))
        tags = random.sample(
            list(models.EventTag.objects.all()), random.randint(1, 5))
        event = models.Event.objects.create(
            name=name,
            location=location,
            location_url=location_url,
            description=description,
            full_description=full_description,
            type=type,
            start_date=start_date,
            end_date=end_date,
            author=author,
        )
        event.tags.set(tags)
        path = settings.MEDIA_ROOT + random.choice(EVENT_FILES)
        event.image.save(f'{name}.png', File(open(path, 'rb')))
        event.save()
        for i in range(agendas):
            name = random.choice(AGENDA_NAMES)
            start_date = event.start_date + \
                datetime.timedelta(hours=random.randint(0, 24))

            models.AgendaItem.objects.create(
                name=name,
                event=event,
                start_date=start_date,
            )
        for skill in REQUIRED_SKILLS:
            models.RequiredSkill.objects.create(
                name=skill,
            )
        for name in TEAM_NAMES:
            t_name = name + " " + event.name
            leader = random.choice(
                models.User.objects.filter(is_superuser=True))
            team = models.Team.objects.create(
                name=t_name,
                leader=leader,
                event=event,
            )
            for i in range(random.randint(1, 5)):
                skill = random.choice(
                    list(models.RequiredSkill.objects.all()))
                team.required_skills.add(skill)
            for i in range(random.randint(1, 5)):
                username = f'{team.name} {i}'
                user = models.User.objects.create(
                    username=username,
                    email=f'team_member_{i}_{team.id}@gmail.com',
                )
                path = settings.MEDIA_ROOT + random.choice(USER_AVATARS)
                user.image.save(
                    f'team_member_{i}_{team.id}@gmail.com.png', File(open(path, 'rb')))
                team.members.add(user)

            for i in range(random.randint(1, 5)):
                file = random.choice(EVENT_FILES)
                models.TeamMaterial.objects.create(
                    team=team, file=file, name=f'Important file number {i}')
            for i in range(random.randint(1, 5)):
                url = 'https://www.youtube.com/watch?v=QH2-TGUlwu4'
                models.TeamMaterial.objects.create(
                    team=team, url=url, name=f'Important url number {i}')
            path = settings.MEDIA_ROOT + random.choice(EVENT_FILES)
            team.image.save(f'{name}.png', File(open(path, 'rb')))
            team.save()


def drop_db():

    models.User.objects.all().delete()
    models.Event.objects.all().delete()
    models.EventTag.objects.all().delete()
    models.EventType.objects.all().delete()
    models.AgendaItem.objects.all().delete()
    models.Team.objects.all().delete()
    models.Ticket.objects.all().delete()


class Command(BaseCommand):
    help = 'Generate fake data'

    def handle(self, *args, **options):
        drop_db()
        create_data()
        self.stdout.write(self.style.SUCCESS(
            'Successfully created a fake database'))
