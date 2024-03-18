import re


class CSVReader:
    """ Open the already converted file and read it """

    @staticmethod
    def open_read_file(file_path):
        with open(file_path, 'r') as file:
            content_range = file.readlines()
            CSVFormatter.formatting_csv(file_path, content_range)


class CSVFormatter:
    """ Format CSV files """

    @staticmethod
    def formatting_csv(file_path, content_range):
        """ Format the csv file """

        output_lines = []
        # Indicator whether we are included in the table
        processing_table = False

        for line in content_range:
            """ Iterate through the content range """

            if 'Code' in line:
                # Check if the 'Code' row is a table header and format it
                if re.match(r'^Code.*Total', line.strip()):
                    output_lines.append(line.strip().replace(",,", ","))
                # Indicator whether we are included in the table
                processing_table = True

            elif processing_table:
                CSVFormatter.formatting_table(line, output_lines)
            else:
                output_lines.append(line.strip())

            CSVFormatter.format_outside_table(output_lines)
            CSVWriter.writing_csv(file_path, output_lines)

    @staticmethod
    def formatting_table(line, output_lines):
        """ Format the cell in the table """
        if re.match(r'^\d{2}-', line.strip()):
            # String with REF
            number_pattern = r'(?<=,)(\b\d+(?:,\d{1,2})?\b)(?=,)'
            # Replacing numbers without quotes with numbers in "quotes"
            line1_modified = re.sub(number_pattern, r'"\1"', line.strip())
            # Remove the spaces
            output_lines.append(line1_modified.strip()
                                .replace(",,,,", ",")
                                .replace(",,,", ",")
                                .replace(",,", ","))
        else:
            # Formatting Substring
            if re.match(r'^,\s', line.strip()):
                line = re.sub(r'^,\s', ',', line.strip())

            elif re.match(r'^,,,', line.strip()):
                line = re.sub(r'^,,,', ',', line.strip())

            elif re.match(r'^,,', line.strip()):
                line = re.sub(r'^,,', ',', line.strip())

            matches = re.findall(r'(?<=,)\d+(?=,)', line.strip())
            if matches:
                for match in matches:
                    comma_count = line.count(',', 0, line.index(match))
                    comma_count -= 1
                    line = line.replace(',' * comma_count, ',', 1)

            output_lines.append(line.strip())

    @staticmethod
    def format_outside_table(output_lines):
        """ Format other cells outside the table """

        # Apply styles for the cells
        for i in range(len(output_lines)):
            output_lines[i] = re.sub(r'^,+T\.V\.A\.', ',,,,T.V.A.', output_lines[i])
            output_lines[i] = re.sub(r'^,+Total TVA comprise', ',,,,Total TVA comprise', output_lines[i])
            output_lines[i] = re.sub(r'^,+EUR', ',,,,EUR', output_lines[i])
            output_lines[i] = re.sub(r'EUR,*', 'EUR,', output_lines[i])
            output_lines[i] = re.sub(r'^([^,]*),+Port', r'\1,,,,Port', output_lines[i])

            output_lines[i] = (
                output_lines[i]
                .replace(',:,', ':')
                .replace(':,', ':')
                .replace(',:', ':')
                .replace(':,,', ':')
                .replace(',,:', ':')
                .replace(',N°', ',,,N°')
                .replace(',Vos', ',,,Vos')
                .replace('COMMANDE,,', 'COMMANDE,')
                .replace('Client :,', ',,Client :')
                .replace(' BIC:', ',,,BIC:')
                .replace('TVA,', 'TVA')
                .replace(',,Réf', ',Réf')
                .replace(',POUR ZIP', ' POUR ZIP')
                .replace(',YKK DA2', ' YKK DA2')
                .replace('ZIP YKK 5 PLASTIQUE DETACHABLE', ' YKK DA2')
                .replace(',,Quant.', ',Quant.')
                .replace(',,Prix Unit.', ',Prix Unit.')
                .replace('Unit.,,Total', 'Unit.,Total')
                .replace(',Total hors', ',,Total hors')
                .replace(', 3 Y DA2', ' 3 Y DA2')
                .replace(', 3 METAL YKK DA2', ' 3 METAL YKK DA2')
                .replace(', 3 MM YKK POUR ZIP', ' 3 MM YKK POUR ZIP')
                .replace(',09', '09')
                .replace(',08', '08')
                .replace(',07', '07')
                .replace(',06', '06')
                .replace(',05', '05')
                .replace(',04', '04')
                .replace(',03', '03')
                .replace(',02', '02')
                .replace(',01', '01')
                .replace(',00', '00')
            )


class CSVWriter:
    """ Write output to file """

    @staticmethod
    def writing_csv(file_path, output_lines):
        with open(file_path, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')
