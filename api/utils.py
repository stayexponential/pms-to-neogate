from django.db import connection


def get_custom_sql(organization, filter_type):
    with connection.cursor(using='sql_server') as cursor:
        cursor.execute(your_custom_sql_query)
    base_sql = f"""
    SELECT
        {organization.property_code} AS property,
        'EVENT' AS wifigroup,
        EVM_CONFIRMATIONNUMBER AS account,
        EVM_CONFIRMATIONNUMBER AS room,
        EVM_DESC AS name,
        LOWER(REPLACE(REPLACE(SUBSTRING(evm_desc, 6, 1), ' ', ''), '.', '') + REPLACE(REPLACE(SUBSTRING(evm_desc, 1, 5), ' ', ''), '.', '')) AS password,
        EVM_STATUS AS status,
        EVM_STARTDATE AS arrival,
        EVM_ENDDATE AS departure,
        DATEADD(day, 1, EVM_ENDDATE) AS expired,
        'EVENT' AS reftype,
        EVM_CONFIRMATIONNUMBER AS refno
        FROM P5EVENTMASTER EVM
        LEFT JOIN R5ORGANIZATION ORG
        ON ORG.ORG_CODE = EVM.EVM_PROPERTYCODE
        WHERE EVM_STATUS NOT IN ('CLX','CMPLT','PROS')
        AND EVM_STARTDATE >= ORG.ORG_HOTELDATE

    UNION ALL

    SELECT
        {organization.property_code} AS property,
        'GUEST' AS wirigroup,
        rsl_confirmationnumber AS account,
        rsl_room AS room,
        CASE
            WHEN RSL.rsl_firstname IS NULL AND RSL.rsl_lastname IS NULL THEN 'None'
            WHEN RSL.rsl_firstname = '' AND RSL.rsl_lastname = '' THEN 'None'
            ELSE CONCAT(RSL.rsl_firstname, ' ', RSL.rsl_lastname)
        END AS name,
        LOWER(REPLACE(REPLACE(SUBSTRING(rsl.rsl_lastname, 6, 1), ' ', ''), '.', '') + REPLACE(REPLACE(SUBSTRING(rsl.rsl_lastname, 1, 5), ' ', ''), '.', '')) AS password,
        rsl_status AS status,
        rsl_arrivaldate AS arrival,
        rsl_departuredate AS departure,
        rsl_departuredate AS expired,
        'GUEST' AS reftype,
        rsl_confirmationnumber AS refno
    FROM P5RESERVATIONLIST RSL
    LEFT JOIN R5ORGANIZATION ORG
    ON ORG.ORG_CODE = RSL.rsl_propertycode
    WHERE RSL_STATUS NOT IN ('CHKOUT','CANCELED','NOSHOW','WAITLIST')
    AND rsl_arrivaldate >= ORG.ORG_HOTELDATE;
    """
    return base_sql
