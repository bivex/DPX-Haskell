"""Tests for Native Haskell Parser Adapter."""

from pattern_detector.adapters.outbound.parsers.native_haskell_parser_adapter import NativeHaskellParserAdapter


def test_parse_haskell_types_and_typeclasses():
    source = """
{-# LANGUAGE GADTs, TypeFamilies, DerivingStrategies #-}

module Domain.Core (User(..), Storage(..)) where

import qualified Data.Text as T
import Control.Monad.Reader

newtype UserId = UserId Int
  deriving stock (Show, Eq)
  deriving newtype (Num)

data Expr a where
  I :: Int -> Expr Int
  B :: Bool -> Expr Bool
  Add :: Expr Int -> Expr Int -> Expr Int

class Monad m => MonadDB m where
  type QueryKey m
  fetchUser :: UserId -> m (Maybe T.Text)
  saveUser :: UserId -> T.Text -> m ()

getUser :: UserId -> ReaderT Env IO (Maybe T.Text)
getUser uid = do
  env <- ask
  liftIO $ putStrLn "Fetching"
  pure Nothing
"""
    parser = NativeHaskellParserAdapter()
    module_model = parser.parse_file("Domain/Core.hs", source)

    assert module_model.name == "Domain.Core"
    assert "GADTs" in module_model.pragmas
    assert "TypeFamilies" in module_model.pragmas
    assert "DerivingStrategies" in module_model.pragmas
    assert "Data.Text" in module_model.imports

    # Types
    assert "UserId" in module_model.types
    assert module_model.types["UserId"].is_newtype
    assert "stock" in module_model.types["UserId"].deriving_strategies

    assert "Expr" in module_model.types
    assert module_model.types["Expr"].is_gadt

    # Typeclasses
    assert "MonadDB" in module_model.typeclasses
    tc = module_model.typeclasses["MonadDB"]
    assert len(tc.methods) == 2
    assert "QueryKey" in tc.associated_types

    # Functions
    assert "getUser" in module_model.functions
    fn = module_model.functions["getUser"]
    assert fn.has_do
