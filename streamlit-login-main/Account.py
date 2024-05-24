import streamlit as st
from navigation import make_sidebar
from firebase_admin import credentials, auth, initialize_app, _apps
if not _apps:
    cred = credentials.Certificate('chatpdf-b3260-2b9e8704f1d8.json')
    initialize_app(cred)
make_sidebar()


def app():
    
    st.title('Welcome to :blue[ChatPDF]')

    if"username" not in st.session_state:
       st.session_state.username =""
    if"useremail" not in st.session_state:
       st.session_state.useremail =""

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.write('Welcome ' +user.uid)

            st.session_state.username = user.uid
            st.session_state.useremail = user.email

            st.session_state.signedout=True
            st.session_state.signout=True

        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout=False
        st.session_state.username=''

    if 'signedout' not in st.session_state:
         st.session_state.signedout = False
        
    if 'signout' not in st.session_state:
         st.session_state.signout = False
        
        
    
    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup',['Login','Sign Up'])
        
        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type ='password')
             
            st.button('Login', on_click=f)
        else:
             email = st.text_input('Email Address')
             password = st.text_input('Password' ,type='password')
             username = st.text_input('Enter a  Unique username')
             
             
             
        if st.button('Create my account'):
             user = auth.create_user(email = email,password = password, uid=username)
            
             st.success('Account created successfully!')
             st.markdown('Please Login using your email and password')
             st.balloons()
             
        
        
        
    
    if st.session_state.signout:
        st.text('Name: '+st.session_state.username)
        st.text('Email ID: '+st.session_state.useremail)
        st.button('Sign out',on_click=t)

if __name__ == '__main__':
    app()