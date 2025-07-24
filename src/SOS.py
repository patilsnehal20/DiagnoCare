import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- Your API keys ---
GEOAPIFY_API_KEY = "api_key_here"
TWILIO_ACCOUNT_SID = 'account_sid_here'
TWILIO_AUTH_TOKEN = 'token_id_here'
TWILIO_PHONE_NUMBER = 'phone_no_here'
if st.button("Back"):
    st.switch_page("pages/Utilities.py")

# st.write("🔍 Page loaded successfully.")
def send_sms(hospital_name, hospital_phone):
    try:
        # Clean and validate the phone number
        phone_number = hospital_phone.strip().replace(" ", "")
        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Emergency! Help required at {hospital_name}. Immediate assistance needed.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid

    except Exception as e:
        st.error(f"Failed to send SMS: {str(e)}")
        return None


from twilio.rest import Client


def make_call(to_number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        twiml='<Response><Say>This is an emergency call from your healthcare assistant. Immediate help is needed.</Say></Response>',
        from_=TWILIO_PHONE_NUMBER,
        to=to_number
    )
    return call.sid


def main():
    st.title("Emergency SOS & Hospital Locator")
    location = st.text_input("Enter your location (e.g., Pune, Maharashtra, India):")

    if location:
        # Step 1: Get latitude and longitude
        encoded_location = urllib.parse.quote(location)
        geo_url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_location}&apiKey={GEOAPIFY_API_KEY}"

        geo_response = requests.get(geo_url)

        if geo_response.status_code != 200:
            st.error(f"Failed to get geolocation! (Status Code: {geo_response.status_code})")
            st.stop()

        try:
            geo_data = geo_response.json()
        except Exception as e:
            st.error(f"Error decoding geo_response JSON: {e}")
            st.stop()

        if not geo_data.get("features"):
            st.error("No results found for the entered location.")
            st.stop()

        latitude = geo_data['features'][0]['properties']['lat']
        longitude = geo_data['features'][0]['properties']['lon']

        # Step 2: Find nearby hospitals
        hospital_url = (
            f"https://api.geoapify.com/v2/places?categories=healthcare.hospital&filter=circle:{longitude},{latitude},5000&limit=5&apiKey={GEOAPIFY_API_KEY}"
        )
        hospital_response = requests.get(hospital_url)

        if hospital_response.status_code != 200:
            st.error(f"Failed to get hospitals! (Status Code: {hospital_response.status_code})")
            st.stop()

        try:
            hospital_data = hospital_response.json()
        except Exception as e:
            st.error(f"Error decoding hospital_response JSON: {e}")
            st.stop()

        if not hospital_data.get("features"):
            st.warning("No hospitals found nearby.")
            st.stop()

        # Step 3: Show hospitals on a map
        m = folium.Map(location=[latitude, longitude], zoom_start=13)

        for hospital in hospital_data['features']:
            name = hospital['properties'].get('name', 'Unnamed Hospital')
            lat = hospital['geometry']['coordinates'][1]
            lon = hospital['geometry']['coordinates'][0]

            folium.Marker(
                location=[lat, lon],
                popup=name,
                icon=folium.Icon(color="red", icon="plus-sign"),
            ).add_to(m)

        st.subheader("🏥 Nearby Hospitals Map:")
        st_folium(m, width=700, height=500)

        st.subheader("List of Nearby Hospitals:")
        for idx, hospital in enumerate(hospital_data['features']):
            hospital_name = hospital['properties'].get('name', 'Unnamed Hospital')
            st.write(f"{idx + 1}. {hospital_name}")

        # Step 4: Emergency Call and SMS Section
        st.subheader("Emergency Actions")

        preferred_hospital = st.selectbox(
            "Select hospital for emergency contact:",
            [h['properties'].get('name', 'Unnamed Hospital') for h in hospital_data['features']],
            key="hospital_select"
        )

        phone_number = st.text_input("Enter hospital or emergency phone number:", key="phone_input")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Trigger Emergency Call", key="sos_call_button"):
                if preferred_hospital:
                    st.success(f"Emergency call triggered for {preferred_hospital}!")
                    make_call(phone_number)


        with col2:
            if st.button("✉️ Send Emergency SMS", key="sos_sms_button"):
                if preferred_hospital and phone_number:
                    sid = send_sms(preferred_hospital, phone_number)
                    st.success(f"Emergency message sent successfully to {phone_number}!")
                    st.toast(f"Emergency SMS sent to {preferred_hospital}!", icon="📨")


# Run the app
if __name__ == "__main__":
    main()

