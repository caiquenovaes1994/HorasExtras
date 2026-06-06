
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {Table as RadixThemesTable,Text as RadixThemesText} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_ddc099ed4ee25e66fc36afc40b9eb414 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.registros_agrupados_rx_state_ ?? [],((row_rx_state_,index_cf05a28db47e5d59f8179f75c57895c1)=>(jsx(RadixThemesTable.Row,{key:index_cf05a28db47e5d59f8179f75c57895c1},jsx(RadixThemesTable.Cell,{},row_rx_state_?.["data"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["semana"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["p1"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["p2"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["p3"]),jsx(RadixThemesTable.Cell,{},jsx(RadixThemesText,{as:"p",weight:"bold"},row_rx_state_?.["horas_trabalhadas"])),jsx(RadixThemesTable.Cell,{css:({ ["color"] : "var(--ruby-11)" })},row_rx_state_?.["50%"]),jsx(RadixThemesTable.Cell,{css:({ ["color"] : "var(--ruby-11)" })},row_rx_state_?.["100%"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["caso"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["valor_base_snapshot"])))))
    )
});
