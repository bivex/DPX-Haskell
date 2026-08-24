{-# LANGUAGE TemplateHaskell #-}

module OpticsStreamService where

import Control.Lens
import Control.Concurrent.Async
import Control.Concurrent.STM.TQueue
import Control.Concurrent.STM
import Data.Conduit
import qualified Data.Conduit.List as CL

data Config = Config {
    _host :: String,
    _port :: Int
} deriving (Show, Eq)

makeLenses ''Config

processPipeline :: ConduitT Int Int IO ()
processPipeline = CL.map (* 2) .| CL.filter (> 10)

workerMailbox :: TQueue String -> IO ()
workerMailbox queue = do
  (res1, res2) <- concurrently (pure "Task 1") (pure "Task 2")
  atomically $ writeTQueue queue (res1 ++ res2)
