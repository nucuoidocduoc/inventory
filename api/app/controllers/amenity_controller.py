from flask import Blueprint, make_response
from app.db.mongo.documents.amenity import Amenity
from app.db.mongo.documents.amenity_provider_mapping import AmenityProviderMapping
from app.db.mongo.documents.property import Property

from app.db.mongo.documents.translation import IndexedTranslation

amenity_controller = Blueprint('amenity_controller', __name__)


@amenity_controller.route("/api/seed_amenities", methods=["POST"])
# @abac_authorize()
def seed_amenities():
    amenities = [Amenity(code='1', provider='bamboo', value=[IndexedTranslation(language_code='vi-VN', value='Tour sinh thái')], type='composite'),
                 Amenity(code='2', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Ngâm chân')], type='composite'),
                 Amenity(code='3', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Spa')], type='composite'),
                 Amenity(code='4', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Làm đẹp và trang điểm')], type='composite'),
                 Amenity(code='5', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Chăm sóc cơ thể')], type='composite'),
                 Amenity(code='6', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Nhân viên hành lý')], type='composite'),
                 Amenity(code='7', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Nơi chứa hành lý')], type='composite'),
                 Amenity(code='8', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Gọi điện đánh thức')], type='composite'),
                 Amenity(code='9', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Phòng giặt ủi')], type='composite'),
                 Amenity(code='10', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Dịch vụ giặt là')], type='composite'),
                 Amenity(code='11', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Nhà hàng')], type='composite'),
                 Amenity(code='12', provider='bamboo',
                         value=[IndexedTranslation(language_code='vi-VN', value='Cà phê')], type='composite'),
                 Amenity(code='13', provider='bamboo', value=[IndexedTranslation(language_code='vi-VN', value='Bar')], type='composite')]
    for amenity in amenities:
        amenity.save()
    response = make_response('Success')
    response.status_code = 200
    return response


@amenity_controller.route("/api/seed_amenities_mapping", methods=["POST"])
def seed_amenities_mapping():
    amenities_mapping = [
        AmenityProviderMapping(source_code='1', source_provider='bamboo',
                               destination_code='2043', destination_provider='expedia'),
        AmenityProviderMapping(source_code='2', source_provider='bamboo',
                               destination_code='361', destination_provider='expedia'),
        AmenityProviderMapping(source_code='3', source_provider='bamboo',
                               destination_code='2066', destination_provider='expedia'),
        AmenityProviderMapping(source_code='4', source_provider='bamboo',
                               destination_code='372', destination_provider='expedia'),
        AmenityProviderMapping(source_code='5', source_provider='bamboo',
                               destination_code='3500', destination_provider='expedia'),
        AmenityProviderMapping(source_code='6', source_provider='bamboo',
                               destination_code='4514', destination_provider='expedia'),
        AmenityProviderMapping(source_code='7', source_provider='bamboo',
                               destination_code='2537', destination_provider='expedia'),
        AmenityProviderMapping(source_code='8', source_provider='bamboo',
                               destination_code='3912', destination_provider='expedia'),
        AmenityProviderMapping(source_code='9', source_provider='bamboo',
                               destination_code='385', destination_provider='expedia'),
    ]
    for mapping in amenities_mapping:
        mapping.save()
