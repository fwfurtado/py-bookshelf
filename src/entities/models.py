from sqlalchemy import (  # type: ignore
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    TEXT,
)
from sqlalchemy.orm import relationship  # type: ignore

from src.entities import Base


class Document(Base):  # type: ignore
    name = Column(String(255))
    entry_date = Column(DateTime)
    file_hash = Column(String(255))
    file_extension = Column(String(255))
    file_type = Column(String(255))
    index_hash = Column(String(255))

    optional_document_attributes = relationship(
        "OptionalDocumentAttributes", back_populates="document", lazy="subquery"
    )

    file_paths = relationship(
        "DocumentStorage", back_populates="document", lazy="subquery"
    )


class OptionalDocumentAttributes(Base):  # type: ignore
    document_id = Column(
        Integer, ForeignKey("documents.id"), primary_key=True, nullable=False
    )
    name = Column(String(255), primary_key=True)
    value = Column(String(255), primary_key=True)

    document = relationship(
        "Document", back_populates="optional_document_attributes", lazy="joined"
    )

    def __repr__(self) -> str:
        return (
            f"<OptionalDocumentAttributes("
            f"document_id={self.document_id}, "
            f"name='{self.name}', "
            f"value='{self.value}'>"
            f")"
        )


class DocumentStorage(Base):  # type: ignore
    document_id = Column(
        Integer, ForeignKey("documents.id"), primary_key=True, nullable=False
    )
    storage_engine = Column(String(255), primary_key=True)
    file_path = Column(String(255), primary_key=True)

    document = relationship(
        "Document", back_populates="file_paths", lazy="subquery"
    )

    def __repr__(self) -> str:
        return (
            f"<DocumentStorage("
            f"document_id={self.document_id}, "
            f"storage_engine='{self.storage_engine}', "
            f"file_path='{self.file_path}'"
            f")>"
        )


class ConversionVersion(Base):  # type: ignore
    engine = Column(String(255))
    version: str = Column(String(255))

    def __repr__(self) -> str:
        return (
            f"<ConversionVersion("
            f"id={self.id}, "
            f"engine='{self.engine}', "
            f"version='{self.version}'"
            f")>"
        )


class Conversion(Base):  # type: ignore
    document_id = Column(Integer, ForeignKey("documents.id"))
    conversion_version_id = Column(Integer, ForeignKey("conversion_versions.id"))
    converted_text = Column(TEXT, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    conversion_version = relationship("ConversionVersion", lazy="subquery")
    document = relationship("Document", lazy="subquery")

    def __repr__(self) -> str:
        return (
            f"<Conversion("
            f"id={self.id}, "
            f"document_id={self.document_id}, "
            f"converted_text='{self.converted_text}', "
            f"converted_version_id={self.conversion_version_id}"
            f")>"
        )


class Extraction(Base):  # type: ignore
    document_id = Column(Integer, ForeignKey("documents.id"))
    conversion_id = Column(Integer, ForeignKey("conversions.id"))
    extraction_version_id = Column(Integer, ForeignKey("extraction_versions.id"))
    structured_data = Column(JSON)
    new_structured_data = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    extraction_version = relationship("ExtractionVersion", lazy="subquery")
    document = relationship("Document", lazy="joined")
    conversion = relationship("Conversion", lazy="subquery")

    def __repr__(self) -> str:
        return (
            f"<Extraction("
            f"id={self.id}, "
            f"document_id={self.document_id}, "
            f"conversion_id={self.conversion_id}, "
            f"extraction_version_id={self.extraction_version_id}, "
            f"structured_data={self.new_structured_data}"
            f")>"
        )


class ExtractionVersion(Base):  # type: ignore
    engine = Column(String(255))
    version = Column(String(255))
    tag = Column(String(255))

    def __repr__(self) -> str:
        return (
            f"<ExtractionVersion("
            f"id={self.id}, "
            f"engine='{self.engine}', "
            f"version='{self.version}', "
            f"tag='{self.tag}'"
            f")>"
        )


class ValidationSchema(Base):  # type: ignore

    validation_schema_json = Column(JSON)
    file_type = Column(String(255))

    def __repr__(self) -> str:
        return (
            f"<ValidationSchema("
            f"id={self.id}, "
            f"validation_schema_json={self.validation_schema_json}, "
            f"file_type='{self.file_type}'"
            f")>"
        )


class DoccanoMonocleDocument(Base):  # type: ignore

    monocle_document_id = Column(
        Integer, ForeignKey("documents.id"), primary_key=True, nullable=False
    )
    doccano_document_id = Column(Integer, primary_key=True, nullable=False)
    doccano_project_id = Column(Integer, primary_key=True, nullable=False)
    extraction_version_id = Column(
        Integer, ForeignKey("extraction_versions.id"), nullable=False
    )

    document = relationship("Document", lazy="joined")
    extraction_version = relationship("ExtractionVersion", lazy="joined")

    def __repr__(self) -> str:
        return (
            "<DoccanoMonocleDocument("
            f"monocle_document_id={self.monocle_document_id}, "
            f"doccano_document_id={self.doccano_document_id}, "
            f"extraction_version_id={self.extraction_version_id}"
            ")>"
        )
