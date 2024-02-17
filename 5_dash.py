import pandas as pd 
import streamlit as st
import numpy as np
import jdatetime 
import datetime 
import plotly.express as px 
import warnings 
import re 
import math 
import openpyxl 
import os 
import glob 
import extra_streamlit_components as stx 




# ////////////////////////////// تابع های مورد نیاز
def convert_to_list(t):
    if isinstance(t, list):
        return t
    elif isinstance(t, tuple):
        return list(t)
    else :      # انگار این فقط میگه استرینگ باشه و دیکشنری باشه را اینجوری میده
        return [t]

def farsi_underscore_pd(df):
    new_col=[re.sub(' +','_',colname) for colname in df.columns.tolist() ]   
    df.rename(columns=dict(zip(df.columns,new_col)),inplace=True)
    return df

def jalali_converter_lenmonth(input_month='اسفند',value_want='the_number',):
    the_month=jalali_converter(input_month) # اول تبدیل میکنیم اون ماهه را 
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    month_days={}
    # بعد هر کدوم را میگیم اگه پیش از مهر بود بزار ماه را ۳۱ روزه 
    # اگه ماه ماه بین ۱۲ و ۷ بود ۳۰ روزه 
    # اگه ۱۲ هم بود ۲۹ روزه 
    # البته کبیسه ها را باید بعدا تبدیل کنم 
    for month in month_list:
        if the_month<7  :
            day_list=list(range(1,32))
        elif 7< the_month<12:
            day_list=list( range(1,31))
        elif  the_month==12:
            day_list=list(range(1,30))
        month_days[month] =day_list
    # حالا اگر لیست  روزها را خواست لیست را میده وگرنه که طول و تعداد را میده
    if value_want=='the_list':
        return month_days[input_month]
    elif value_want=='the_number':
        return len(month_days[input_month])




# برای ورودی ها که به مرداد و تیر و.. میده باید برج را اورد
def jalali_converter(input_month=None):
    '''
    :param input_month:  اگر عدد را میدیم و ماه را میخوایم عدد را بصورت اینتیجر یعنی  2 میدیم واگر ماه را به حروف دادیم باید استرینگ باشه یعنی  'فروردین' '
    :return: خروجی عدد بود واژه میده و اگر واژه دادی عدد ماه را میده
    '''
    mah_be_borg={
        'فروردین': 1 ,
        'اردیبهشت':2 ,
        'خرداد':3 ,
        'تیر': 4,
        'مرداد': 5,
        'شهریور':6 ,
        'مهر': 7,
        'آبان':8 ,
        'آذر': 9,
        'دی': 10,
        'بهمن':11 ,
        'اسفند':12 ,
    }
    # اینم تبدیل برج به ماه
    borg_be_mah={ val:key for key , val in mah_be_borg.items()}
    if isinstance(input_month,str):
        return mah_be_borg[input_month]
    elif isinstance(input_month,int):
        return borg_be_mah[input_month]
# jalli_converter('مرداد')  #5
# jalli_converter('مرداد')  #5
# jalli_converter(7) # 'مهر'




# تابعی که تاریخ جلالی را با سلکت میسازه و خروجی را میده تاریخ انتخاب شده را میده به صورت جلالی یا میلادی


# تابعی که تاریخ جلالی را با سلکت میسازه و خروجی را میده تاریخ انتخاب شده را میده به صورت جلالی یا میلادی
def calender_selected_jalali_st(col1,
                                title='از چه بازه زمانی',
                                frmt='gr',
                                identifier='', # کلید های مختلفی از یک تابع با این میشه ساخت
                                the_size=18,
                                
                                alignment = 'center',
                                color='blue',
                                default_day='today'
                               ):
    
    
    
    # این کلیدو میاریم که این ارور DuplicateWidgetID را نخوریم و یگانه باشند هر کلید
    year_widget_id = f"{title}_year_{identifier}"
    month_widget_id = f"{title}_month_{identifier}"
    day_widget_id = f"{title}_day_{identifier}"
    
    
    
    
    col1.markdown(f"<h2 style='font-size:{the_size}px; text-align:{alignment}; color:{color};'>{title}:</h2>",
                  unsafe_allow_html=True) 
    
    
    now_time=jdatetime.datetime.now()
    year_list=list(range(1380,1420))
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    #  اینجا هم کلید را میاره که یگانه باشه
    year=col1.selectbox('برگزیدن سال',year_list,index=year_list.index(now_time.year),key=year_widget_id) # تعین دیفالت
    month=col1.selectbox( 'برگزیدن ماه' ,month_list,index=month_list.index(jalali_converter(now_time.month)),key=month_widget_id)
    # اون روزی که انتخاب میشه . اون بازه زمانی میاد بر اساس ماه
    
    
    day_list=jalali_converter_lenmonth(input_month=month,value_want='the_list')
    # اینو میزنیم که ماه ها که پیشفرضشون روی روزی است و عوض بشن دیگه مشکل نداشته باشن و امتحان کنه و نشد خودش بزاره روی اخری
    
    # زمان اکنون را برمیگزینیم
    if default_day=='today':
        try:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( now_time.day),key=day_widget_id)
        except:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( day_list[-1]),key=day_widget_id )
            
    elif default_day=='yesterday':
        try:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (now_time.day)-1),key=day_widget_id)
        except:
            day=col1.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (day_list[-1])-1),key=day_widget_id )
            
        
    

    # تبدیل چیزی که اانتخاب شده به فرمت ها
    selected_date_jl=jdatetime.datetime.strptime(f"{year}/{jalali_converter(month)}/{day}","%Y/%m/%d" )
    selected_date_gr=pd.to_datetime(selected_date_jl.togregorian()).date()
    selected_date_jl=selected_date_jl.date()
    #col1.write(selected_date_jl)
    #col1.write(selected_date_gr)
    
    if frmt=='gr':
        return selected_date_gr # هم میسازه و هم برمیگردونه موقع فراخوانی
    elif frmt=='jl':
        return selected_date_jl



# تابعی میخوام که ورودی را بگیره پس از اون خروجیش را طبق لیستی که دادیم برمیگردونه
# به همون ترتیب که ورودی بود. یعنی اگر داخل پرانتز بود رجکس میکنه برمیگردونش 
def sarparast_supervisor_correct(correct_list,case_list,
                                 demand='correct_value',
                                 mode_on='dataframe'):
    # از تابع تصحیح گر استفاده کردیم
    # که چه لیست داد چه یه اسم خالی داد برش گردونه به چیزی که میگیم 
    correct_list, case_list = (convert_to_list(char) for char in (correct_list, case_list))    
    # اینم طبق اردر دیکت زدیم که ترتیب بهم نخوره
    output={}
    # روی تک تک اعضای لیست معیار
    for the_case in case_list:
        # تک تک اعضای مورد را بررسی کن
        for the_correct in correct_list:
            # با روش سرچ برو بگرد اگر اون مورد بود پیدا شد 
            if re.search(the_correct, the_case): 
                # اونو بریز ولیو کن  که کلیدش اون غلطه باشه
                output[the_case] = the_correct
                # تا پیدا کردی دیگه بقیه را ادامه نده بشکونش
                break
        else:
            # اگر نبود ولیو را خالی کن جلوی اون مورد که نیست در معیار
            output[the_case] = None
    # return(output)
    # حالا اگر در بالا نوشته بودیم کارت ولیو را لیست کن ولیو ها را برگردون
    if demand=='correct_value':
        if mode_on=='dataframe':
            # اینکه روی صفر باشه اولین عنصرشو میده که خوب تبعا چون با لیست میشه اولین عنصر یه لیست خالی میشه لیست
            return list(output.values())[0]
        elif mode_on=='list_tuple':
            return list(output.values())
    # اینو که صفر کنیم درست میشه ولی فقط اولیشو میده اگر بخوایم دوتا لیست را تبدیل کنیم
    
    # این دیکشنری را میده
    # یعنی غلطه به عنوان کلید و درسته به عنوان ولیو میشه
    elif demand=='dict':
        return output


# ///////////




warnings.filterwarnings('ignore')
st.set_page_config(page_title='آمار تبلیغات همکده',
                  page_icon=':bar_chart',)

title_page='آمار تبلیغات همکده'
alignment='center'
# ;color:{color};
color='white'
font_size=30
st.markdown(f"<h1 style='font-size:{font_size};text-align:{alignment};'>{title_page}</h1>",
           unsafe_allow_html=True
           )







# ////////////

# توی کش میزاریم که سریع تر بیاره بالا
@st.cache_data
def read_load_xlsx():
    sabt_mahsul=pd.read_excel('files//factorsExtraction(135).xlsx')
    sabt_hamkade=pd.read_excel('files//factorsExport (3).xlsx')
    estexarj_hamkade=pd.read_excel('files//ExtractionEntriesExport (35).xlsx')
    estexarj_mahsul=pd.read_excel('files//extractionEntries(31).xlsx')
    hamkade_amel_person = pd.read_excel('files//گزارش تبلیغات21.11.xlsx', sheet_name='Base-hamkade')
    return sabt_mahsul , sabt_hamkade ,estexarj_hamkade,estexarj_mahsul,hamkade_amel_person

sabt_mahsul, sabt_hamkade, estexarj_hamkade, estexarj_mahsul, hamkade_amel_person = read_load_xlsx()

for excel in [sabt_hamkade,sabt_mahsul,estexarj_hamkade,estexarj_mahsul]:
    farsi_underscore_pd(excel) 

# اول اونایی که ان ای دارند در هر دوستون در این ستون ها را بردار بعد همون ستون ها را بیار
hamkade_ameliat=hamkade_amel_person.dropna(subset=['عاملیت','Unnamed: 8'],how='all')[['عاملیت','Unnamed: 8']]
hamkade_person=hamkade_amel_person.dropna(subset=['مجری','فرد'])[['مجری','فرد']]
hamkade_ameliat.rename(columns={'Unnamed: 8':'شبکه_مجازی'},inplace=True)


drop_list_hamkade_vosul=[ 'شماره_مراجع', 'نام_مراجع',  'مبلغ_قبل_از_تخفیف',  'شماره_رسید', 'آشنایی_با_ما', 'نوع_فاکتور','ثبت_کننده_اطلاعات_واریزی', 'شناسه_نوبت_مربوطه','پورسانت','زمان_ثبت_اطلاعات_واریزی','تاریخ_لغو_شده', 'لغو_کننده',  'بررسی_کننده_اطلاعات_واریزی']
sabt_hamkade.drop([ col for col in drop_list_hamkade_vosul ],axis=1,inplace=True)
# sabt_hamkade 
vosul_hamkade=sabt_hamkade.loc[sabt_hamkade['وضعیت_وصولی'].isin(['تایید شده']) 
                &sabt_hamkade['نوع_پرداخت'].isin(['درگاه پرداخت','کارت به کارت'])
                &sabt_hamkade['وضعیت_فاکتور'].isin(['پرداخت شده'] )].reset_index(drop=True)
vosul_hamkade['مبلغ_فاکتور']=(vosul_hamkade['مبلغ_فاکتور']/10).astype(int)


# /////////




estexarj_hamkade['تاریخ_ورود_جلالی']=estexarj_hamkade['تاریخ_ورود'].apply(lambda x :
                                     jdatetime.datetime.strptime(f"{x.split()[2]}{'-'}{jalali_converter(x.split()[1])}{'-'}{x.split()[0]}{' '}{x.split()[3]}",
                                                                 "%Y-%m-%d %H:%M:%S"))
estexarj_hamkade['تاریخ_ورود_میلادی']=estexarj_hamkade['تاریخ_ورود'].apply(lambda x :pd.to_datetime(jdatetime.datetime.strptime(f"{x.split()[2]}{'-'}{jalali_converter(x.split()[1])}{'-'}{x.split()[0]}{' '}{x.split()[3]}",
                                                                 "%Y-%m-%d %H:%M:%S").togregorian()))
estexarj_hamkade['تاریخ_ورود_میلادی_روزانه']=estexarj_hamkade['تاریخ_ورود'].apply(lambda x :pd.to_datetime(jdatetime.datetime.strptime(f"{x.split()[2]}{'-'}{jalali_converter(x.split()[1])}{'-'}{x.split()[0]}{' '}{x.split()[3]}", "%Y-%m-%d %H:%M:%S").togregorian()).date()) 

estexarj_hamkade['تاریخ_ورود_جلالی_روزانه']=estexarj_hamkade['تاریخ_ورود'].apply(lambda x :
                                     jdatetime.datetime.strptime(f"{x.split()[2]}{'-'}{jalali_converter(x.split()[1])}{'-'}{x.split()[0]}{' '}{x.split()[3]}", "%Y-%m-%d %H:%M:%S").date() )

estexarj_hamkade ['تاریخ_ورود_روزانه']=estexarj_hamkade ['تاریخ_ورود_جلالی_روزانه'].apply(lambda x : jdatetime.datetime.strftime(x,'%Y-%m-%d'))

# /////////

estexarj_hamkade=estexarj_hamkade.sort_values(by='تاریخ_ورود_میلادی')
# estexarj_hamkade 
df_hamkade_ex=pd.merge(estexarj_hamkade,hamkade_ameliat,on=['عاملیت'],how='left')
# df_hamkade_ex

df_hamkade_ex[['تعداد_تماس_جواب_داده','تعداد_کل_تماس']]=df_hamkade_ex[['تعداد_تماس_جواب_داده','تعداد_کل_تماس']].fillna(0)
# df_hamkade_ex 


df_hamkade_ex_vosul=pd.merge(df_hamkade_ex,vosul_hamkade[['نوع_پرداخت','ثبت_کننده','نوع_فاکتور.1','مبلغ_فاکتور','سریال_فاکتور','موضوع_فاکتور']],on='سریال_فاکتور',how='left')


drop_list_hamkade_vosul=[  'متن_پیامک' , 'سامانه_پیامک','ویزیتور' ,
                         'موبایل']
df_hamkade_ex_vosul.drop([ col for col in drop_list_hamkade_vosul ],axis=1,inplace=True)


# همه را کانورت میکنیم  به دیکشنری که اسم لیستشونو تنها با صدا زدن بیاریم
df_hamkade_ex_vosul.rename(columns={'نوع_فاکتور.1':'نوع_فاکتور'},inplace=True)
lists_name_dict= {lists:df_hamkade_ex_vosul[lists].unique().tolist() for lists in ['عاملیت','شبکه_مجازی','نوع_فاکتور','نوع_پرداخت']}


pd.set_option('display.max_columns',500)


# ///////

col1,col2,col3,col4=st.columns(4)

# /// ساید بار
col1=st.sidebar

# kartabl_dasti=col1.multiselect(label ='کارتابلی یا دستی را برگزینید' ,
#                                options =lists_name_dict['نوع_فاکتور'],
#                                default =convert_to_list((lists_name_dict['نوع_فاکتور'][2])),placeholder='نوع فاکتور را برگزینید')

# dargah_kart=col1.multiselect(label ='نوع پرداخت را برگزینید' ,
#                              options =lists_name_dict['نوع_پرداخت'],
#                              default=convert_to_list((lists_name_dict['نوع_پرداخت'][2],lists_name_dict['نوع_پرداخت'][3])),
#                              placeholder=' نوع پرداخت را برگزینید')


# network=col1.multiselect(label ='عاملیت را برگزینید' ,
#                          options =lists_name_dict['عاملیت'],
#                          default=lists_name_dict['عاملیت'],
#                          placeholder=' عاملیت را برگزینید')



after_sidebar_df=df_hamkade_ex_vosul.copy()
# df_hamkade_ex_vosul.loc[ df_hamkade_ex_vosul['شبکه_مجازی'].isin(network) 
                                                    # &df_hamkade_ex_vosul['نوع_پرداخت'].isin(dargah_kart) 
                                                    # &df_hamkade_ex_vosul['شبکه_مجازی'].isin(network) 
                                                    # &df_hamkade_ex_vosul['عاملیت'].isin(ameliat)  
                                                    # ]






# ////////// تاریخ 

the_to=calender_selected_jalali_st(col1=col2,title='تا چه بازه زمانی',identifier='to',color='#00FFFF',default_day='today')
the_from=calender_selected_jalali_st(col1=col3,title='از چه بازه زمانی' ,identifier='from',color='#00FFFF',default_day='yesterday')

after_date_df=df_hamkade_ex_vosul[df_hamkade_ex_vosul['تاریخ_ورود_میلادی_روزانه'].between(the_from,the_to)].sort_values(by='تاریخ_ورود_میلادی_روزانه')


# این عاملیت ها را میشماره چندبار در هر روز بکار رفتن و مبلغشونو میشماره 
df_count_sum = pd.DataFrame()
for the_tuple in (('شبکه_مجازی', 'count'),
                  ('مبلغ_فاکتور', 'sum')):
    new = after_date_df.groupby(['عاملیت','تاریخ_ورود_جلالی_روزانه', 'تاریخ_ورود_میلادی_روزانه','تاریخ_ورود_روزانه','شبکه_مجازی'])[the_tuple[0]].agg([the_tuple[1]])
    df_count_sum = pd.concat([df_count_sum, new], axis=1)
    df_count_sum.rename(columns={the_tuple[1]:( 'تعداد_شماره_ورودی' if the_tuple[1] =='count' else 'جمع_مبلغ_وصولی')},inplace=True)
df_count_sum.reset_index(inplace=True) 


network=st.multiselect(label='شبکه_مجازی را برگزینید' , 
                         options= lists_name_dict['شبکه_مجازی'],
                        default=convert_to_list((lists_name_dict['شبکه_مجازی'][1])),
                         placeholder=' شبکه_مجازی را برگزینید')

# st.write(network)  
# [
# 0:
# "گوگل ادز "
# 1:
# "پیامکی (لینکی)"
# ]
# for value in df_count_sum['شبکه_مجازی'].unique().tolist():  # این از اول همه را میاره
ameliat={} 
try:
    for value in network:   # این اونایی که انتخاب شده اند است
        # st.write (value) گوگل ادز
        ameliat[value]= col1.multiselect(f'عاملیت های {value} را برگزینید',
                                            options= df_count_sum.groupby('شبکه_مجازی')['عاملیت'].unique().to_dict()[value].tolist() ,
                                            default= df_count_sum.groupby('شبکه_مجازی')['عاملیت'].unique().to_dict()[value].tolist() ,
                                            placeholder=f'هیچ {value} برگزیده نشده'
                                           )
except KeyError: 
    st.info(f' این بازه تاریخی و مورد برگزیده شده هیچ داده ای ندارد')
    
# after_sidebar_df=df_count_sum.loc[ 
#                                     df_count_sum['عاملیت'].isin(ameliat) &
#                                     df_count_sum['شبکه_مجازی'].isin(network) 
# ]
ameliat_all_val=[val for values in ameliat.values() for val in values]  # این همه ولیو ها را میاره میریزه تو یه لیست که بعد گروپ بای کنیمش
# st.write (network) 
# st.write(ameliat_all_val) 

# این همه را میاره  عاملیت ها را هم میاره
after_sidebar_df=df_count_sum.loc[df_count_sum['عاملیت'].isin(ameliat_all_val) &
                                df_count_sum['شبکه_مجازی'].isin(network) ]

# st.write(after_sidebar_df) 



st.markdown("""
    <style>
    .stRadio [role=radiogroup] {
        align-items: center;
        justify-content: center;
    }
    </style>
""",
    unsafe_allow_html=True)


radio_count_sum=st.radio(
   '',
    options=[":rainbow[تعداد_شماره_ورودی]",":rainbow[جمع_مبلغ_وصولی]"],
    index=1,
    horizontal=True,
)

radio_oprator=st.radio(
   '',
    options=["بنابرعاملیت🕵️‍♀️"
             ,"بنابر شبکه مجازی🌍"],
    index=1,
    horizontal=True,
)

if radio_oprator =="بنابرعاملیت🕵️‍♀️":
    if radio_count_sum==":rainbow[جمع_مبلغ_وصولی]":
        fig=px.line(after_sidebar_df , x='تاریخ_ورود_جلالی_روزانه', 
                                       y='جمع_مبلغ_وصولی', 
                                        color='عاملیت', 
                    hover_data=[
                                 'جمع_مبلغ_وصولی'
                                # ,'تعداد_شماره_ورودی'
                                # ,'عاملیت'
                                ,'شبکه_مجازی'
                                ,'تاریخ_ورود_جلالی_روزانه'
                    ])
                   
        fig.update_xaxes(title_text='تاریخ_روز',tickangle=-45,tickformat='%Y-%m-%d')
        st.plotly_chart(fig)
        st.write(after_sidebar_df ) 

    elif radio_count_sum==":rainbow[تعداد_شماره_ورودی]":
        fig=px.line(after_sidebar_df , x='تاریخ_ورود_جلالی_روزانه', 
                                       y='تعداد_شماره_ورودی', 
                                        color='عاملیت', 
                    
                    hover_data=[  'تعداد_شماره_ورودی',# 
                                'شبکه_مجازی',
                                # 'عاملیت', 
                                'تاریخ_ورود_جلالی_روزانه',
                                ])
                   
        fig.update_xaxes(title_text='تاریخ_روز',tickangle=-45,tickformat='%Y-%m-%d')
        st.plotly_chart(fig)
        
        st.write(after_sidebar_df ) 
    
if radio_oprator =="بنابر شبکه مجازی🌍":

    if radio_count_sum ==":rainbow[جمع_مبلغ_وصولی]":
        
        net_sum=after_sidebar_df.groupby(['شبکه_مجازی','تاریخ_ورود_جلالی_روزانه','تاریخ_ورود_میلادی_روزانه'])['جمع_مبلغ_وصولی'].agg(['sum']).reset_index() 
        net_sum.rename(columns={'sum':'جمع_مبلغ_وصولی'},inplace=True)
        fig=px.line(net_sum , x='تاریخ_ورود_جلالی_روزانه', 
                                       y='جمع_مبلغ_وصولی', 
                                        color='شبکه_مجازی', 
                    hover_data=[
                                 'جمع_مبلغ_وصولی'
                                # ,'تعداد_شماره_ورودی'
    
                                ,'شبکه_مجازی'
                                ,'تاریخ_ورود_جلالی_روزانه'
                    ])
                   
        fig.update_xaxes(title_text='تاریخ_روز',tickangle=-45,tickformat='%Y-%m-%d')
        st.plotly_chart(fig)
        st.write(after_sidebar_df ) 
        
    elif radio_count_sum==":rainbow[تعداد_شماره_ورودی]":
        net_count=after_sidebar_df.groupby(['شبکه_مجازی','تاریخ_ورود_جلالی_روزانه','تاریخ_ورود_میلادی_روزانه'])['تعداد_شماره_ورودی'].agg(['sum']).reset_index() 
        net_count.rename(columns={'sum':'تعداد_شماره_ورودی'},inplace=True)
        fig=px.line(net_count , x='تاریخ_ورود_جلالی_روزانه', 
                                       y='تعداد_شماره_ورودی', 
                                        color='شبکه_مجازی', 
                    
                    hover_data=[  'تعداد_شماره_ورودی',# 
                                'شبکه_مجازی',
                                # 'عاملیت', 
                                'تاریخ_ورود_جلالی_روزانه',
                                ])
                   
        fig.update_xaxes(title_text='تاریخ_روز',tickangle=-45,tickformat='%Y-%m-%d')
        st.plotly_chart(fig)
        
        st.write(net_count ) 
