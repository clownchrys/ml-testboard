type MenuItemType = {
  path: string,
  name: string
}

export type MenuGroupType = {
  root: MenuItemType,
  children: MenuItemType[]
}
