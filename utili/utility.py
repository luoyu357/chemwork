""""
Developer Name : Tarini Dash<tdash@iu.edu>
Date : 10/18/2021
Description : This program is a utilty package
"""


def transform_biblio(biblio):
    new_biblio = {}
    if 'doi' in biblio:
        new_biblio['doi'] = biblio['doi']
    if 'published_date' in biblio:
        new_biblio['published_date'] = biblio['published_date']
    if 'title' in biblio:
        new_biblio['title'] = biblio['title']
    return new_biblio


def validate_record(record):
    if ('electrochemical_potentials' in record
            or 'fluorescence_lifetimes' in record
            or 'quantum_yields' in record
            or 'uvvis_spectra' in record):
        return True
    else:
        return False


def apply_rules(records, config):
    new_records = []
    elec_chem_min_range = float(config.get("validation", "elec_chem_min_range"))
    elec_chem_max_range = float(config.get("validation", "elec_chem_max_range"))
    flur_lif_time_min_range = float(config.get("validation", "flur_lif_time_min_range"))
    flur_lif_time_max_range = float(config.get("validation", "flur_lif_time_max_range"))
    qtum_ylds_min_range = float(config.get("validation", "qtum_ylds_min_range"))
    qtum_ylds_max_range = float(config.get("validation", "qtum_ylds_max_range"))
    uv_spec_pks_extn_min_range = float(config.get("validation", "uv_spec_pks_extn_min_range"))
    uv_spec_pks_extn_max_range = float(config.get("validation", "uv_spec_pks_extn_max_range"))
    uv_spec_pks_units = config.get("validation", "uv_spec_pks_units")
    uv_spec_pks_val_min_range = float(config.get("validation", "uv_spec_pks_val_min_range"))
    uv_spec_pks_val_max_range = float(config.get("validation", "uv_spec_pks_val_max_range"))
    em_spec_pks_val_min_range = float(config.get("validation", "em_spec_pks_val_min_range"))
    em_spec_pks_val_max_range = float(config.get("validation", "em_spec_pks_val_max_range"))

    for record in records:
        if validate_record(record):
            if 'ir_spectra' in record:
                del record['ir_spectra']
            if 'labels' in record:
                del record['labels']
            if 'melting_points' in record:
                del record['melting_points']
            if 'nmr_spectra' in record:
                del record['nmr_spectra']
            if 'roles' in record:
                del record['roles']
            if 'electrochemical_potentials' in record:
                for es in record['electrochemical_potentials']:
                    if 'value' in es:
                        if not elec_chem_min_range <= float(es['value'].replace('–', '-').replace(',', '')) <= elec_chem_max_range:
                            es['value_validation_failed'] = "1"
            if 'fluorescence_lifetimes' in record:
                for fl in record['fluorescence_lifetimes']:
                    if 'value' in fl:
                        if not flur_lif_time_min_range <= float(
                                fl['value'].replace('–', '-').replace(',', '')) <= flur_lif_time_max_range:
                            fl['value_validation_failed'] = "1"
            if 'quantum_yields' in record:
                for qy in record['quantum_yields']:
                    if 'value' in qy:
                        if not qtum_ylds_min_range <= float(qy['value'].replace('–', '-').replace(',', '')) <= qtum_ylds_max_range:
                            qy['value_validation_failed'] = "1"
            if 'uvvis_spectra' in record:
                for uvs in record['uvvis_spectra']:
                    for peaks in uvs['peaks']:
                        if 'extinction' in peaks:
                            if not uv_spec_pks_extn_min_range <= float(
                                    peaks['extinction'].replace('–', '-').replace(',', '')) <= uv_spec_pks_extn_max_range:
                                peaks['extinction_validation_failed'] = "1"
                        if 'units' in peaks:
                            if not peaks['units'] == uv_spec_pks_units:
                                peaks['units_validation_failed'] = "1"
                        if 'value' in peaks:
                            if not uv_spec_pks_val_min_range <= float(
                                    peaks['value'].replace('–', '-').replace(',', '')) <= uv_spec_pks_val_max_range:
                                peaks['value_validation_failed'] = "1"
            if 'emisn_spectra' in record:
                for ems in record['emisn_spectra']:
                    for peaks in ems['peaks']:
                        if 'value' in peaks:
                            if not em_spec_pks_val_min_range <= float(
                                    peaks['value'].replace('–', '-').replace(',', '')) <= em_spec_pks_val_max_range:
                                peaks['value_validation_failed'] = "1"

            new_records.append(record)

    return new_records