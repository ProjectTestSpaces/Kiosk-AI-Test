# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: inventory_service.proto
# Protobuf Python Version: 6.30.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    0,
    '',
    'inventory_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17inventory_service.proto\x12\tinventory\"N\n\x16InventoryUpdateRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x0e\n\x06\x61\x63tion\x18\x03 \x01(\t\"*\n\x17InventoryUpdateResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2l\n\x10InventoryService\x12X\n\x0fUpdateInventory\x12!.inventory.InventoryUpdateRequest\x1a\".inventory.InventoryUpdateResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'inventory_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INVENTORYUPDATEREQUEST']._serialized_start=38
  _globals['_INVENTORYUPDATEREQUEST']._serialized_end=116
  _globals['_INVENTORYUPDATERESPONSE']._serialized_start=118
  _globals['_INVENTORYUPDATERESPONSE']._serialized_end=160
  _globals['_INVENTORYSERVICE']._serialized_start=162
  _globals['_INVENTORYSERVICE']._serialized_end=270
# @@protoc_insertion_point(module_scope)
