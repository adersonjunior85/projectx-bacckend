from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.adapters.database import engine
from app.enums.toll_voucher_status_types import TollVoucherStatusTypes
from app.models.entities import Address, Shipper, TollVoucher, Vehicle
from app.models.toll_voucher import (
    TollVoucherBase,
    TollVoucherCreate,
    TollVoucherListRead,
    TollVoucherRead,
    TollVoucherUpdate,
)
from app.repositories.base_repository import BaseRepository


class TollVoucherRepository(BaseRepository[TollVoucherBase]):
    def __init__(self, session: Session = None) -> None:
        if session:
            self.session = session
        else:
            self.session = Session(engine)

    def create(self, entity: TollVoucherCreate) -> TollVoucher:
        with self.session as session:
            destination_address = Address.model_validate(entity.destination)
            origin_address = Address.model_validate(entity.origin)
            entity.vehicle = Vehicle.model_validate(entity.vehicle)
            entity.shipper = Shipper.model_validate(entity.shipper)

            toll_voucher = TollVoucher(
                origin_address_id=origin_address.id,
                destination_address_id=destination_address.id,
                **vars(entity),
            )

            session.add(destination_address)
            session.add(origin_address)

            # Cria VPO como rascunho
            toll_voucher.status = TollVoucherStatusTypes.DRAFT
            session.add(toll_voucher)

            session.commit()
            session.refresh(toll_voucher)

        return toll_voucher

    def get_list(self, params: dict) -> List[TollVoucherListRead]:
        offset, limit = params["offset"], params["limit"]

        with self.session as session:
            results = session.exec(
                select(TollVoucher).offset(offset).limit(limit)
            )
            voucher_list = []
            for voucher in results:
                voucher_list.append(
                    TollVoucherListRead(
                        id=voucher.id,
                        identifier=voucher.identifier,
                        code=voucher.code,
                        status=voucher.status,
                        emission_date=voucher.emission_date,
                        vehicle_plate=voucher.vehicle.plate,
                        provider=voucher.vehicle.toll_voucher_provider,
                    )
                )

        return voucher_list

    def get_by_id(self, id_: UUID) -> TollVoucherRead | None:
        with self.session as session:
            db_voucher = session.get(TollVoucher, id_)

            origin = session.get(Address, db_voucher.origin_address_id)
            destination = session.get(
                Address, db_voucher.destination_address_id
            )

            # Necessário para obter os objetos em lazy-load
            session.refresh(db_voucher.vehicle)
            session.refresh(db_voucher.shipper)

            voucher = TollVoucherRead(
                origin=origin,
                destination=destination,
                **vars(db_voucher),
            )

        return voucher

    def update(self, entity: TollVoucherUpdate) -> TollVoucher | None:
        with self.session as session:
            db_voucher = session.get(TollVoucher, entity.id)
            if db_voucher is None:
                raise HTTPException(
                    status_code=404, detail="Voucher not found"
                )
            voucher_data = entity.model_dump(exclude_unset=True)
            db_voucher.sqlmodel_update(voucher_data)
            session.add(db_voucher)
            session.commit()
            session.refresh(db_voucher)

            return db_voucher

    def cancel_by_id(self, id_: UUID) -> None:
        with self.session as session:
            db_voucher = session.get(TollVoucher, id_)
            if not db_voucher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"TollVoucher with ID {id_} not found",
                )

            db_voucher.status = TollVoucherStatusTypes.CANCELED
            session.add(db_voucher)
            session.commit()
            session.refresh(db_voucher)

    def delete_by_id(self, id_: UUID) -> None:
        with self.session as session:
            db_voucher = session.get(TollVoucher, id_)
            if not db_voucher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"TollVoucher with ID {id_} not found",
                )

            session.delete(db_voucher)
            session.commit()
