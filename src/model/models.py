from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from sqlalchemy.ext.associationproxy import association_proxy

from src.model.base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cd_barras = Column(String(20), unique=True, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, nullable=False, default=True)

    itens_venda = relationship("ItemVenda", back_populates="produto")
    """ movimentacoes = relationship(
        "MovimentacaoEstoque",
        back_populates="produto"
    ) """


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(20))
    

    vendas = relationship("Venda", back_populates="cliente")


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True)
    valor_total = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    data = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Cliente é opcional
    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=True,
    )

    cliente = relationship("Cliente", back_populates="vendas")
    itens = relationship(
        "ItemVenda",
        back_populates="venda",
        cascade="all, delete-orphan",
    )


class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True)

    venda_id = Column(
        Integer,
        ForeignKey("vendas.id"),
        nullable=False,
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False,
    )

    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_venda")

    nome = association_proxy("produto", "nome")


""" class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"

    id = Column(Integer, primary_key=True)

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False,
    )

    quantidade = Column(Integer, nullable=False)

    # E = Entrada | S = Saída
    tipo = Column(String(1), nullable=False)

    data = Column(DateTime, nullable=False, default=datetime.utcnow)

    produto = relationship(
        "Produto",
        back_populates="movimentacoes",
    ) """