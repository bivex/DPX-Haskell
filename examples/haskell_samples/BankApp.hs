{-# LANGUAGE GADTs, TypeFamilies, DerivingStrategies, OverloadedStrings, GeneralizedNewtypeDeriving #-}

module BankApp (
    Account(..),
    AccountId(..),
    Money(..),
    Transaction(..),
    BankEnv(..),
    BankM,
    transferFunds,
    runBankM
) where

import Control.Concurrent.STM
import Control.Monad.Reader
import Control.Monad.Except
import qualified Data.Text as T
import Data.Maybe (fromJust)

-- DDD Strong Types
newtype AccountId = AccountId { unAccountId :: Int }
  deriving stock (Show, Eq, Ord)
  deriving newtype (Num)

newtype Money = Money { unMoney :: Integer }
  deriving stock (Show, Eq, Ord)
  deriving newtype (Num, Real, Enum, Integral)

-- Domain GADT
data Transaction a where
  Deposit  :: AccountId -> Money -> Transaction ()
  Withdraw :: AccountId -> Money -> Transaction Bool
  Balance  :: AccountId -> Transaction Money

-- Bank Account Model with STM TVar
data Account = Account {
    accId      :: AccountId,
    accBalance :: TVar Money
}

-- Application Environment (ReaderT Pattern)
data BankEnv = BankEnv {
    envDbConn    :: T.Text,
    envLogHandle :: T.Text
}

-- Layered Monad Transformer Stack: ExceptT + ReaderT + IO
type BankM a = ExceptT T.Text (ReaderT BankEnv IO) a

runBankM :: BankEnv -> BankM a -> IO (Either T.Text a)
runBankM env action = runReaderT (runExceptT action) env

-- Composable STM Concurrency
transferFunds :: Account -> Account -> Money -> IO (Either T.Text ())
transferFunds fromAcc toAcc amount = atomically $ do
  fromBal <- readTVar (accBalance fromAcc)
  if fromBal < amount
    then retry
    else do
      writeTVar (accBalance fromAcc) (fromBal - amount)
      toBal <- readTVar (accBalance toAcc)
      writeTVar (accBalance toAcc) (toBal + amount)
      pure (Right ())
