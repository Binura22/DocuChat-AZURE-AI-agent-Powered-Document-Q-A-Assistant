name: str = "Global Tech Solutions Inc."
address: str = "456 Digital Avenue, Silicon Valley, CA 94025"
contact: str = "+1-555-0123"
email: str = "info@globaltechsolutions.com"
website: str = "https://www.globaltechsolutions.com"
privacy_policy: str = f"{website}/privacy"
terms_and_conditions: str = f"{website}/terms"
mission: str = "Empowering businesses with cutting-edge technology solutions that drive growth and innovation."
vision: str = "To create a digitally transformed world where technology enhances every aspect of business operations."
values: list[str] = [
    "Excellence in Service",
    "Technological Innovation",
    "Client Partnership",
    "Ethical Business Practices",
    "Continuous Learning"
]

details = {
    "name": name,
    "address": address,
    "contact": contact,
    "email": email,
    "website": website,
    "privacy_policy": privacy_policy,
    "terms_and_conditions": terms_and_conditions,
    "mission": mission,
    "vision": vision,
    "values": values
}


def get_company_details():
    return details