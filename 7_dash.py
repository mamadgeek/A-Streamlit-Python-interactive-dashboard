



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

from back_functions import *


# /////////////

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



col1,col2,col3,col4=st.columns(4)


# ///////////




























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




after_sidebar_df=df_hamkade_ex_vosul.copy()

# ////////// تاریخ 




the_from=Jalali_Streamlit_calendar( 
    st_col=col3, 
    title='از چه بازه زمانی', 
    frmt='gr', 
    identifier='' ,# کلید های مختلفی از یک تابع با این میشه ساخت
    the_size=18,
    
    alignment = 'center',
    color='cyan',
    default_day='today',
    format_datetime='datetime',
    
    step_min=1,
    default_min='sefr' ,
    # default_min='aknun' 
    # default_min=('before_after',-2) ,
    
    
    # default_hour='aknun_h' ,
    default_hour='sefr_h' ,
    # default_hour=('before_after_h',-2) 
    step_hour=1)


the_to=Jalali_Streamlit_calendar(
    st_col=col2,
    title='تا چه بازه زمانی',
    frmt='gr',
    identifier='' ,# کلید های مختلفی از یک تابع با این میشه ساخت
    the_size=18,
    
    alignment = 'center',
    color='red',
    default_day='today',
    format_datetime='datetime',
    
    step_min=1,
    default_min='sefr' ,
    # default_min='aknun' 
    # default_min=('before_after',-2) ,
    
    
    default_hour='aknun_h' ,
    # default_hour='sefr_h' ,
    # default_hour=('before_after_h',-2) ,
    step_hour=1)




col5=st.sidebar
dict_unit={'دقیقه':'min','ثانیه':'s','ساعت':'h','روز':'d'}
choice_unit=col5.selectbox('یگان زمانی را برگزینید',options=list(dict_unit.keys()),index=3)
# choice_unit='روز'
interval =col5.selectbox(f' هرچند {choice_unit}',options=list(range(1,61)),index=0)


# name=f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"
df_hamkade_ex_vosul[f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"]=df_hamkade_ex_vosul["تاریخ_ورود_میلادی"].apply(lambda x :
                                                                         x.ceil(freq =f"{interval}{dict_unit[choice_unit]}")
                                                                         if choice_unit=='دقیقه'  else 
                                                                         x.floor(freq =f"{interval}{dict_unit[choice_unit]}")  ) 





df_hamkade_ex_vosul[f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}"]=df_hamkade_ex_vosul[f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"].apply(lambda x:(jdatetime.datetime.fromgregorian(year=x.year,month=x.month,day=x.day ,hour=x.hour ,minute=x.minute,second=x.second )))


df_hamkade_ex_vosul[f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}_استرینگ"]=df_hamkade_ex_vosul[f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}"].apply(lambda x: jdatetime.datetime.strftime(x,'%Y-%m-%d %H:%M:%S')  )






after_date_df=df_hamkade_ex_vosul[df_hamkade_ex_vosul[f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"].between(the_from,the_to)].sort_values(by=f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}")



# st.write(after_date_df)





# این عاملیت ها را میشماره چندبار در هر روز بکار رفتن و مبلغشونو میشماره 
df_count_sum = pd.DataFrame()
for the_tuple in (('شبکه_مجازی', 'count'),
                  ('مبلغ_فاکتور', 'sum')):
    new = after_date_df.groupby(['عاملیت',f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}", f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}",f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}_استرینگ",'شبکه_مجازی'])[the_tuple[0]].agg([the_tuple[1]])
    df_count_sum = pd.concat([df_count_sum, new], axis=1)
    df_count_sum.rename(columns={the_tuple[1]:( 'تعداد_شماره_ورودی' if the_tuple[1] =='count' else 'جمع_مبلغ_وصولی')},inplace=True)
df_count_sum.reset_index(inplace=True) 







network=st.multiselect(label='شبکه_مجازی را برگزینید' , 
                         options= lists_name_dict['شبکه_مجازی'],
                        default=convert_to_list((lists_name_dict['شبکه_مجازی'][1])),
                         placeholder=' شبکه_مجازی را برگزینید')








# /////////////////




ameliat={} 
try:
    for value in network:   # این اونایی که انتخاب شده اند است
        # st.write (value) گوگل ادز
        ameliat[value]= col5.multiselect(f'عاملیت های {value} را برگزینید',
                                            options= df_count_sum.groupby('شبکه_مجازی')['عاملیت'].unique().to_dict()[value].tolist() ,
                                            default= df_count_sum.groupby('شبکه_مجازی')['عاملیت'].unique().to_dict()[value].tolist() ,
                                            placeholder=f'هیچ {value} برگزیده نشده'
                                           )
except KeyError: 
    st.info(f' این بازه تاریخی و مورد برگزیده شده هیچ داده ای ندارد')
    


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
    options=["بنابرعاملیت🕵️‍♀️",
             "بنابر شبکه مجازی🌍"],
    index=1,
    horizontal=True,) 





if radio_oprator =="بنابرعاملیت🕵️‍♀️":
    if radio_count_sum==":rainbow[جمع_مبلغ_وصولی]":
        fig=px.line(after_sidebar_df , x=f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}", 
                                       y='جمع_مبلغ_وصولی', 
                                        color='عاملیت', 
                                        markers=True ,
                    hover_data=[
                                 'جمع_مبلغ_وصولی'
                                # ,'تعداد_شماره_ورودی'
                                # ,'عاملیت'
                                ,'شبکه_مجازی'
                                ,f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}"
                    ])
                   
        fig.update_xaxes(title_text=f"تاریخ_ورود_هر_{interval}_{choice_unit}",tickangle=-45,tickformat='%Y-%m-%d %H:%M:%S')
        st.plotly_chart(fig)
        st.write(after_sidebar_df)
    elif radio_count_sum==":rainbow[تعداد_شماره_ورودی]":
        fig=px.line(after_sidebar_df , x=f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}", 
                                       y='تعداد_شماره_ورودی', 
                                        color='عاملیت', 
                                        markers=True ,
                    
                    hover_data=[  'تعداد_شماره_ورودی',# 
                                'شبکه_مجازی',
                                # 'عاملیت', 
                                f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}",
                                ])
                   
        fig.update_xaxes(title_text=f"تاریخ_ورود_هر_{interval}_{choice_unit}",tickangle=-45,tickformat='%Y-%m-%d %H:%M:%S')
        st.plotly_chart(fig)
        st.write(after_sidebar_df)
    
if radio_oprator =="بنابر شبکه مجازی🌍":
    if radio_count_sum ==":rainbow[جمع_مبلغ_وصولی]":
        
        net_sum=after_sidebar_df.groupby(['شبکه_مجازی',f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}",f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"])['جمع_مبلغ_وصولی'].agg(['sum']).reset_index() 
        net_sum.rename(columns={'sum':'جمع_مبلغ_وصولی'},inplace=True)
        fig=px.line(net_sum , x=f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}", 
                                       y='جمع_مبلغ_وصولی', 
                                        color='شبکه_مجازی', 
                                        markers=True ,
                    hover_data=[
                                 'جمع_مبلغ_وصولی'
                                # ,'تعداد_شماره_ورودی'
    
                                ,'شبکه_مجازی'
                                ,f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}"
                    ])
                   
        fig.update_xaxes(title_text=f"تاریخ_ورود_هر_{interval}_{choice_unit}",tickangle=-45,tickformat='%Y-%m-%d %H:%M:%S')
        st.plotly_chart(fig)
        st.write(net_sum ) 
        
    elif radio_count_sum==":rainbow[تعداد_شماره_ورودی]":
        net_count=after_sidebar_df.groupby(['شبکه_مجازی',f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}",f"تاریخ_ورود_میلادی_هر_{interval}_{choice_unit}"])['تعداد_شماره_ورودی'].agg(['sum']).reset_index() 
        net_count.rename(columns={'sum':'تعداد_شماره_ورودی'},inplace=True)
        
        fig=px.line(net_count , x=f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}", 
                                       y='تعداد_شماره_ورودی', 
                                        color='شبکه_مجازی', 
                                    markers=True ,
                    
                    hover_data=[  'تعداد_شماره_ورودی',# 
                                'شبکه_مجازی',
                                # 'عاملیت', 
                                f"تاریخ_ورود_جلالی_هر_{interval}_{choice_unit}",
                                ])
                   
        fig.update_xaxes(title_text=f"تاریخ_ورود_هر_{interval}_{choice_unit}",tickangle=-45,tickformat='%Y-%m-%d %H:%M:%S')
        st.plotly_chart(fig)
        st.write(net_count)
     
    
