CREATE TABLE IF NOT EXISTS visa_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- INSERT INTO visa_types (name, description)
-- VALUES
--     (
--         'Tourist Visa',
--         'Issued to individuals travelling for tourism, leisure, or recreational purposes.'
--     ),
--     (
--         'Student Visa',
--         'Issued to individuals travelling to undertake an approved course of study or academic programme.'
--     ),
--     (
--         'Work Visa',
--         'Issued to individuals who are authorised to undertake employment or professional activities in the destination country.'
--     ),
--     (
--         'Business Visa',
--         'Issued to individuals travelling for business-related activities, including meetings, conferences, or commercial engagements.'
--     ),
--     (
--         'Transit Visa',
--         'Issued to individuals who need to pass through a country while travelling to another destination.'
--     ),
--     (
--         'Family Visa',
--         'Issued to individuals travelling to join, visit, or reside with eligible family members in the destination country.'
--     ),
--     (
--         'Medical Visa',
--         'Issued to individuals travelling to obtain medical treatment, consultation, or related healthcare services.'
--     )
-- ON CONFLICT (name) DO NOTHING;