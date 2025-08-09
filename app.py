import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from PIL import Image
import os
import uuid

# Set page configuration
st.set_page_config(page_title="Bike Builder Checklist", layout="wide")

# Database setup
def init_db():
    conn = sqlite3.connect('bike_checklist.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bike_checklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            color TEXT NOT NULL,
            serial_number TEXT NOT NULL,
            tighten_headset BOOLEAN,
            adjust_kickstand BOOLEAN,
            attach_wheel BOOLEAN,
            tightened_axels BOOLEAN,
            installed_fender_headlight BOOLEAN,
            adjust_cockpit_controls BOOLEAN,
            attached_pedals BOOLEAN,
            installed_seat BOOLEAN,
            installed_rear_rack_taillights BOOLEAN,
            install_battery BOOLEAN,
            turn_on_test_bike BOOLEAN,
            adjusted_brakes BOOLEAN,
            adjusted_derailluers BOOLEAN,
            tires_aired BOOLEAN,
            set_speed_20mph BOOLEAN,
            tighten_critical_fasteners BOOLEAN,
            test_ride BOOLEAN,
            charged_battery BOOLEAN,
            notes TEXT,
            technician_name TEXT NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Function to save form data
def save_checklist(data):
    conn = sqlite3.connect('bike_checklist.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO bike_checklist (
            model, color, serial_number, 
            tighten_headset, adjust_kickstand, attach_wheel, tightened_axels,
            installed_fender_headlight, adjust_cockpit_controls, attached_pedals,
            installed_seat, installed_rear_rack_taillights, install_battery,
            turn_on_test_bike, adjusted_brakes, adjusted_derailluers, tires_aired,
            set_speed_20mph, tighten_critical_fasteners, test_ride, charged_battery,
            notes, technician_name, date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['model'], data['color'], data['serial_number'],
        data['tighten_headset'], data['adjust_kickstand'], data['attach_wheel'], data['tightened_axels'],
        data['installed_fender_headlight'], data['adjust_cockpit_controls'], data['attached_pedals'],
        data['installed_seat'], data['installed_rear_rack_taillights'], data['install_battery'],
        data['turn_on_test_bike'], data['adjusted_brakes'], data['adjusted_derailluers'], data['tires_aired'],
        data['set_speed_20mph'], data['tighten_critical_fasteners'], data['test_ride'], data['charged_battery'],
        data['notes'], data['technician_name'], data['date'], data['status']
    ))
    
    conn.commit()
    conn.close()
    return True

# Function to load checklist records
def load_checklists():
    conn = sqlite3.connect('bike_checklist.db')
    query = "SELECT * FROM bike_checklist ORDER BY date DESC, id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to update status
def update_status(record_id, new_status):
    conn = sqlite3.connect('bike_checklist.db')
    c = conn.cursor()
    c.execute("UPDATE bike_checklist SET status = ? WHERE id = ?", (new_status, record_id))
    conn.commit()
    conn.close()

# Initialize session state for form reset
def initialize_form_state():
    if 'form_reset_key' not in st.session_state:
        st.session_state.form_reset_key = str(uuid.uuid4())

# Clear form by changing the reset key
def reset_form():
    st.session_state.form_reset_key = str(uuid.uuid4())

# Main app
def main():
    # Display logo if it exists (try multiple possible locations)
    potential_logo_paths = [
        "electrfied.jpg",
        os.path.join(os.getcwd(), "electrfied.jpg"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "electrfied.jpg")
    ]
    
    logo_found = False
    for logo_path in potential_logo_paths:
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(logo, width=150)
                with col2:
                    st.title("Bike Builder Checklist")
                logo_found = True
                break
            except Exception as e:
                st.error(f"Error loading logo: {e}")
                continue
    
    if not logo_found:
        st.title("Bike Builder Checklist")
        st.warning("Logo file 'electrfied.jpg' not found. Please add it to the app directory.")
    
    # Create tabs for form and view records
    tab1, tab2 = st.tabs(["New Checklist", "View Records"])
    
    # Initialize session state for form reset
    initialize_form_state()
    
    with tab1:
        with st.form(key=f"checklist_form_{st.session_state.form_reset_key}"):
            col1, col2 = st.columns(2)
            
            # Basic bike information
            with col1:
                model = st.text_input("Model", key=f"model_{st.session_state.form_reset_key}")
                color = st.text_input("Color", key=f"color_{st.session_state.form_reset_key}")
                serial_number = st.text_input("Serial #", key=f"serial_{st.session_state.form_reset_key}")
                
                st.subheader("Status")
                status = st.selectbox(
                    "Current Status",
                    options=["In Progress", "Charging", "Ready for the Floor"],
                    key=f"status_{st.session_state.form_reset_key}"
                )
                
                st.subheader("Technician Information")
                technician_name = st.text_input("Technician Name", key=f"name_{st.session_state.form_reset_key}")
                date = st.date_input("Date", datetime.now(), key=f"date_{st.session_state.form_reset_key}")
            
            # Checkboxes for the build checklist
            with col2:
                st.subheader("Build Checklist")
                tighten_headset = st.checkbox("Tighten Headset", key=f"headset_{st.session_state.form_reset_key}")
                adjust_kickstand = st.checkbox("Adjust Kickstand/Height", key=f"kickstand_{st.session_state.form_reset_key}")
                attach_wheel = st.checkbox("Attach Wheel", key=f"wheel_{st.session_state.form_reset_key}")
                tightened_axels = st.checkbox("Tightened Axels", key=f"axels_{st.session_state.form_reset_key}")
                installed_fender_headlight = st.checkbox("Installed Fender/Headlight", key=f"fender_{st.session_state.form_reset_key}")
                adjust_cockpit_controls = st.checkbox("Adjust Cockpit Controls", key=f"cockpit_{st.session_state.form_reset_key}")
                attached_pedals = st.checkbox("Attached Pedals", key=f"pedals_{st.session_state.form_reset_key}")
                installed_seat = st.checkbox("Installed Seat", key=f"seat_{st.session_state.form_reset_key}")
                installed_rear_rack_taillights = st.checkbox("Installed Rear Rack/Taillights", key=f"rack_{st.session_state.form_reset_key}")
                install_battery = st.checkbox("Install Battery", key=f"battery_{st.session_state.form_reset_key}")
                turn_on_test_bike = st.checkbox("Turn on/Test bike", key=f"test_{st.session_state.form_reset_key}")
                adjusted_brakes = st.checkbox("Adjusted Brakes", key=f"brakes_{st.session_state.form_reset_key}")
                adjusted_derailluers = st.checkbox("Adjusted Derailluers", key=f"derailluers_{st.session_state.form_reset_key}")
                tires_aired = st.checkbox("Tires aired", key=f"tires_{st.session_state.form_reset_key}")
                set_speed_20mph = st.checkbox("Set Speed to 20mph", key=f"speed_{st.session_state.form_reset_key}")
                tighten_critical_fasteners = st.checkbox("Tighten All Critical Fasteners", key=f"fasteners_{st.session_state.form_reset_key}")
                test_ride = st.checkbox("Test Ride", key=f"ride_{st.session_state.form_reset_key}")
                charged_battery = st.checkbox("Charged Battery", key=f"charged_{st.session_state.form_reset_key}")
            
            # Notes section
            st.subheader("Notes")
            notes = st.text_area("Additional Notes", key=f"notes_{st.session_state.form_reset_key}", height=150)
            
            # Submit button
            submitted = st.form_submit_button("Save Checklist")
            
            if submitted:
                if not model or not color or not serial_number or not technician_name:
                    st.error("Please fill in all required fields: Model, Color, Serial #, and Technician Name")
                else:
                    # Collect all form data
                    form_data = {
                        'model': model,
                        'color': color,
                        'serial_number': serial_number,
                        'tighten_headset': tighten_headset,
                        'adjust_kickstand': adjust_kickstand,
                        'attach_wheel': attach_wheel,
                        'tightened_axels': tightened_axels,
                        'installed_fender_headlight': installed_fender_headlight,
                        'adjust_cockpit_controls': adjust_cockpit_controls,
                        'attached_pedals': attached_pedals,
                        'installed_seat': installed_seat,
                        'installed_rear_rack_taillights': installed_rear_rack_taillights,
                        'install_battery': install_battery,
                        'turn_on_test_bike': turn_on_test_bike,
                        'adjusted_brakes': adjusted_brakes,
                        'adjusted_derailluers': adjusted_derailluers,
                        'tires_aired': tires_aired,
                        'set_speed_20mph': set_speed_20mph,
                        'tighten_critical_fasteners': tighten_critical_fasteners,
                        'test_ride': test_ride,
                        'charged_battery': charged_battery,
                        'notes': notes,
                        'technician_name': technician_name,
                        'date': date.isoformat(),
                        'status': status
                    }
                    
                    # Save to database
                    if save_checklist(form_data):
                        st.success("Checklist saved successfully!")
                        # Reset the form by changing the form key
                        reset_form()
                        st.rerun()
    
    with tab2:
        st.subheader("Saved Records")
        
        # Load and display records
        try:
            df = load_checklists()
            if not df.empty:
                # Apply color coding to status
                def color_status(status):
                    if status == "Charging":
                        return 'background-color: #ffcccc'  # Red background
                    elif status == "Ready for the Floor":
                        return 'background-color: #ccffcc'  # Green background
                    return ''
                
                # Display a more compact view with key information
                view_df = df[['id', 'model', 'color', 'serial_number', 'technician_name', 'date', 'status']]
                st.dataframe(view_df.style.applymap(color_status, subset=['status']), use_container_width=True)
                
                # Allow detailed view of a selected record
                selected_id = st.selectbox("Select record ID to view details:", options=df['id'].tolist())
                if selected_id:
                    record = df[df['id'] == selected_id].iloc[0]
                    
                    # Add status update functionality
                    col_status1, col_status2 = st.columns([1, 3])
                    with col_status1:
                        current_status = record['status']
                        new_status = st.selectbox(
                            "Update Status:", 
                            options=["In Progress", "Charging", "Ready for the Floor"],
                            index=["In Progress", "Charging", "Ready for the Floor"].index(current_status)
                        )
                    with col_status2:
                        if new_status != current_status:
                            if st.button("Update Status"):
                                update_status(selected_id, new_status)
                                st.success(f"Status updated to: {new_status}")
                                st.rerun()
                    
                    st.subheader(f"Details for Bike: {record['model']} (ID: {record['id']})")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Model:** {record['model']}")
                        st.write(f"**Color:** {record['color']}")
                        st.write(f"**Serial #:** {record['serial_number']}")
                        st.write(f"**Status:** {record['status']}")
                        st.write(f"**Technician:** {record['technician_name']}")
                        st.write(f"**Date:** {record['date']}")
                        
                        st.subheader("Notes")
                        st.write(record['notes'])
                    
                    with col2:
                        st.subheader("Completed Tasks")
                        checklist_items = [
                            ('Tighten Headset', 'tighten_headset'),
                            ('Adjust Kickstand/Height', 'adjust_kickstand'),
                            ('Attach Wheel', 'attach_wheel'),
                            ('Tightened Axels', 'tightened_axels'),
                            ('Installed Fender/Headlight', 'installed_fender_headlight'),
                            ('Adjust Cockpit Controls', 'adjust_cockpit_controls'),
                            ('Attached Pedals', 'attached_pedals'),
                            ('Installed Seat', 'installed_seat'),
                            ('Installed Rear Rack/Taillights', 'installed_rear_rack_taillights'),
                            ('Install Battery', 'install_battery'),
                            ('Turn on/Test bike', 'turn_on_test_bike'),
                            ('Adjusted Brakes', 'adjusted_brakes'),
                            ('Adjusted Derailluers', 'adjusted_derailluers'),
                            ('Tires aired', 'tires_aired'),
                            ('Set Speed to 20mph', 'set_speed_20mph'),
                            ('Tighten All Critical Fasteners', 'tighten_critical_fasteners'),
                            ('Test Ride', 'test_ride'),
                            ('Charged Battery', 'charged_battery')
                        ]
                        
                        for label, key in checklist_items:
                            value = record[key]
                            icon = "✅" if value else "❌"
                            st.write(f"{icon} {label}")
            else:
                st.info("No records found in the database.")
        except Exception as e:
            st.error(f"Error loading records: {e}")

if __name__ == "__main__":
    main()
