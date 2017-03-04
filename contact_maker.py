def make_vcf(first_name, last_name, phone_number):
    """
    Given a first name, last name, and phone number, creates a vcard file (.vcf)
    with their contact information
    """

    # read the template file
    with open('/home/bobby/Flask/Flask/template.vcf', 'r') as template:
        vcard_data = template.read().format(first_name=first_name,
                                            last_name=last_name, phone_number=phone_number)

    # creates a new .vcf file under the persons name with their contact info
    write_path = '/vcf/{}_{}.vcf'.format(first_name, last_name)
    with open(write_path, 'w') as vcf:
        vcf.write(vcard_data)
    file_name = '{}_{}.vcf'.format(first_name, last_name)
    return file_name
