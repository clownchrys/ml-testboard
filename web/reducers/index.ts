import { combineReducers } from "redux";
import menu from "./menu";
import table from "./table";
import render from "./render";

const rootReducer = combineReducers({
  menu,
  table,
  render,
})

export default rootReducer;

export type RootState = ReturnType<typeof rootReducer>;
