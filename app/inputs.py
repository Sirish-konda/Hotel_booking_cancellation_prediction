import streamlit as st
import pandas as pd
import datetime

def get_user_input():
    st.header("🏨 Booking Details")

    # Top summary row
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        arrival_date = st.date_input("Arrival date", value=datetime.date.today(), help="Pick check-in date")
    with c2:
        stays_in_week_nights = st.number_input("Week nights", 0, 30, 3, help="Mon–Thu nights count")
    with c3:
        stays_in_weekend_nights = st.number_input("Weekend nights", 0, 10, 1, help="Fri–Sun nights count")
    with c4:
        auto_lead = st.toggle("Auto lead time (from today)", value=True, help="Compute lead time as days until arrival")

    # Compute derived calendar features to meet model expectations
    arrival_date_month = arrival_date.month
    arrival_date_week_number = arrival_date.isocalendar()[1]
    arrival_date_day_of_month = arrival_date.day

    # Lead time
    if auto_lead:
        lead_time = max(0, (arrival_date - datetime.date.today()).days)
    else:
        lead_time = st.number_input("Lead Time (days)", 0, 1000, 50)

    # Guest & price
    st.subheader("👥 Guests & Price")
    g1, g2, g3, g4, g5 = st.columns([1,1,1,1,1])
    with g1:
        adults = st.number_input("Adults", 1, 10, 2)
    with g2:
        children = st.number_input("Children", 0.0, 10.0, 0.0, step=0.5)
    with g3:
        babies = st.number_input("Babies", 0, 10, 0)
    with g4:
        adr = st.number_input("ADR (€)", 0.0, 1000.0, 100.0, help="Average Daily Rate")
    with g5:
        number_of_bookings = st.number_input("Past bookings (total)", 1, 10, 1)

    # Booking history & requests (expander)
    with st.expander("📝 Booking history & requests"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            previous_cancellations = st.number_input("Previous cancellations", 0, 10, 0)
        with c2:
            previous_bookings_not_canceled = st.number_input("Prev. non-canceled", 0, 10, 0)
        with c3:
            booking_changes = st.number_input("Booking changes", 0, 10, 0)
        with c4:
            days_in_waiting_list = st.number_input("Days in waiting list", 0, 365, 0)

        c5, c6 = st.columns(2)
        with c5:
            total_of_special_requests = st.number_input("Special requests", 0, 10, 0)
        with c6:
            required_car_parking_spaces = st.number_input("Parking spaces", 0, 5, 0)

        is_repeated_guest_1 = st.checkbox("Repeated guest?", value=False)

    # Hotel & segments
    st.subheader("🏨 Hotel & Segments")
    h1, h2, h3 = st.columns(3)
    with h1:
        hotel_Resort_Hotel = st.checkbox("Resort hotel?", value=True)

        deposit_type = st.selectbox("Deposit type", ["No Deposit", "Non Refund", "Refundable"])
        deposit_type_Non_Refund = deposit_type == "Non Refund"
        deposit_type_Refundable = deposit_type == "Refundable"

        customer_type = st.selectbox("Customer type", ["Group", "Transient", "Transient-Party"])
        customer_type_Group = customer_type == "Group"
        customer_type_Transient = customer_type == "Transient"
        customer_type_Transient_Party = customer_type == "Transient-Party"

    with h2:
        meal_type = st.selectbox("Meal plan", ["FB", "HB", "SC", "Undefined"])
        meal_FB = meal_type == "FB"
        meal_HB = meal_type == "HB"
        meal_SC = meal_type == "SC"
        meal_Undefined = meal_type == "Undefined"

        distribution_channel = st.selectbox("Distribution channel", ["Direct", "GDS", "TA/TO", "Undefined"])
        distribution_channel_Direct = distribution_channel == "Direct"
        distribution_channel_GDS = distribution_channel == "GDS"
        distribution_channel_TA_TO = distribution_channel == "TA/TO"
        distribution_channel_Undefined = distribution_channel == "Undefined"

    with h3:
        market_segment = st.selectbox(
            "Market segment",
            ["Complementary", "Corporate", "Direct", "Groups", "Offline TA/TO", "Online TA", "Undefined"]
        )
        market_segment_Complementary = market_segment == "Complementary"
        market_segment_Corporate = market_segment == "Corporate"
        market_segment_Direct = market_segment == "Direct"
        market_segment_Groups = market_segment == "Groups"
        market_segment_Offline = market_segment == "Offline TA/TO"
        market_segment_Online = market_segment == "Online TA"
        market_segment_Undefined = market_segment == "Undefined"

    # Room & region (expander)
    with st.expander("🛏️ Room & Region"):
        reserved_room_type = st.selectbox("Reserved room type", list("BCDEFGHL"))
        reserved_room_type_B = reserved_room_type == "B"
        reserved_room_type_C = reserved_room_type == "C"
        reserved_room_type_D = reserved_room_type == "D"
        reserved_room_type_E = reserved_room_type == "E"
        reserved_room_type_F = reserved_room_type == "F"
        reserved_room_type_G = reserved_room_type == "G"
        reserved_room_type_H = reserved_room_type == "H"
        reserved_room_type_L = reserved_room_type == "L"

        region = st.selectbox("Region", ["Asia", "Europe", "North America", "Oceania", "Other", "South America"])
        region_Asia = region == "Asia"
        region_Europe = region == "Europe"
        region_North_America = region == "North America"
        region_Oceania = region == "Oceania"
        region_Other = region == "Other"
        region_South_America = region == "South America"

    # Build the dataframe your model expects
    data = {
        "lead_time": [lead_time],
        "arrival_date_month": [arrival_date_month],
        "arrival_date_week_number": [arrival_date_week_number],
        "arrival_date_day_of_month": [arrival_date_day_of_month],
        "stays_in_weekend_nights": [stays_in_weekend_nights],
        "stays_in_week_nights": [stays_in_week_nights],
        "adults": [adults],
        "children": [children],
        "babies": [babies],
        "previous_cancellations": [previous_cancellations],
        "previous_bookings_not_canceled": [previous_bookings_not_canceled],
        "booking_changes": [booking_changes],
        "days_in_waiting_list": [days_in_waiting_list],
        "adr": [adr],
        "required_car_parking_spaces": [required_car_parking_spaces],
        "total_of_special_requests": [total_of_special_requests],
        "number_of_bookings": [number_of_bookings],
        "hotel_Resort Hotel": [hotel_Resort_Hotel],
        "meal_FB": [meal_FB],
        "meal_HB": [meal_HB],
        "meal_SC": [meal_SC],
        "meal_Undefined": [meal_Undefined],
        "market_segment_Complementary": [market_segment_Complementary],
        "market_segment_Corporate": [market_segment_Corporate],
        "market_segment_Direct": [market_segment_Direct],
        "market_segment_Groups": [market_segment_Groups],
        "market_segment_Offline TA/TO": [market_segment_Offline],
        "market_segment_Online TA": [market_segment_Online],
        "market_segment_Undefined": [market_segment_Undefined],
        "distribution_channel_Direct": [distribution_channel_Direct],
        "distribution_channel_GDS": [distribution_channel_GDS],
        "distribution_channel_TA/TO": [distribution_channel_TA_TO],
        "distribution_channel_Undefined": [distribution_channel_Undefined],
        "is_repeated_guest_1": [is_repeated_guest_1],
        "reserved_room_type_B": [reserved_room_type_B],
        "reserved_room_type_C": [reserved_room_type_C],
        "reserved_room_type_D": [reserved_room_type_D],
        "reserved_room_type_E": [reserved_room_type_E],
        "reserved_room_type_F": [reserved_room_type_F],
        "reserved_room_type_G": [reserved_room_type_G],
        "reserved_room_type_H": [reserved_room_type_H],
        "reserved_room_type_L": [reserved_room_type_L],
        "deposit_type_Non Refund": [deposit_type_Non_Refund],
        "deposit_type_Refundable": [deposit_type_Refundable],
        "customer_type_Group": [customer_type_Group],
        "customer_type_Transient": [customer_type_Transient],
        "customer_type_Transient-Party": [customer_type_Transient_Party],
        "region_Asia": [region_Asia],
        "region_Europe": [region_Europe],
        "region_North America": [region_North_America],
        "region_Oceania": [region_Oceania],
        "region_Other": [region_Other],
        "region_South America": [region_South_America],
    
}

    user_friendly = {
        "Lead Time (days)": lead_time,
        "Arrival Month": arrival_date_month,
        "Arrival Week": arrival_date_week_number,
        "Arrival Day": arrival_date_day_of_month,
        "Weekend Nights": stays_in_weekend_nights,
        "Week Nights": stays_in_week_nights,
        "Adults": adults,
        "Children": children,
        "Babies": babies,
        "Previous Cancellations": previous_cancellations,
        "Prev Non-Canceled": previous_bookings_not_canceled,
        "Booking Changes": booking_changes,
        "Days in Waiting List": days_in_waiting_list,
        "ADR (€)": adr,
        "Parking Spaces": required_car_parking_spaces,
        "Special Requests": total_of_special_requests,
        "Total Bookings": number_of_bookings,
        "Hotel Type": "Resort Hotel" if hotel_Resort_Hotel else "City Hotel",
        "Meal Type": meal_type,
        "Market Segment": market_segment,
        "Distribution Channel": distribution_channel,
        "Repeated Guest?": "Yes" if is_repeated_guest_1 else "No",
        "Reserved Room Type": reserved_room_type,
        "Deposit Type": deposit_type,
        "Customer Type": customer_type,
        "Region": region,
    }

    return pd.DataFrame(data), user_friendly
