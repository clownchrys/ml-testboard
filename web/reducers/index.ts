import { combineReducers } from "redux";
import menu from "./menu";
import table from "./table";

const rootReducer = combineReducers({
  menu,
  table,
})

export default rootReducer;

export type RootState = ReturnType<typeof rootReducer>;
