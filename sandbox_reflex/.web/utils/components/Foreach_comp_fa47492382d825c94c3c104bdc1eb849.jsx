
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {Table as RadixThemesTable} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_fa47492382d825c94c3c104bdc1eb849 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.registros_agrupados_rx_state_ ?? [],((row_rx_state_,index_b89a42421fd62c21d7e586ff7dad16f2)=>(jsx(RadixThemesTable.Row,{key:index_b89a42421fd62c21d7e586ff7dad16f2},jsx(RadixThemesTable.Cell,{},row_rx_state_?.["data"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["caso"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["hotel"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["motivo"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["inicio"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["termino"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["observacoes"])))))
    )
});
