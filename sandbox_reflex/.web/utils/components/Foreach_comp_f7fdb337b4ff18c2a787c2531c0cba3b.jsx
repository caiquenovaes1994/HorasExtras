
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Button as RadixThemesButton,Checkbox as RadixThemesCheckbox,Flex as RadixThemesFlex,Table as RadixThemesTable,Text as RadixThemesText} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_f7fdb337b4ff18c2a787c2531c0cba3b = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.registros_agrupados_rx_state_ ?? [],((row_rx_state_,index_35443d00308960cec5e253a03392b2ec)=>(jsx(RadixThemesTable.Row,{key:index_35443d00308960cec5e253a03392b2ec},jsx(RadixThemesTable.Cell,{},jsx(RadixThemesText,{as:"label",size:"2"},jsx(RadixThemesFlex,{gap:"2"},jsx(RadixThemesCheckbox,{checked:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.selected_records_rx_state_.includes(row_rx_state_?.["id"]),onCheckedChange:((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.toggle_record", ({ ["record_id"] : row_rx_state_?.["id"], ["is_checked"] : _ev_0 }), ({  })))], [_ev_0], ({  })))),size:"2"},),""))),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["data"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["caso"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["hotel"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["motivo"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["inicio"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["termino"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["observacoes"]),jsx(RadixThemesTable.Cell,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"2"},jsx(RadixThemesButton,{css:({ ["padding"] : "0", ["fontSize"] : "1rem", ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.view_record", ({ ["record_id"] : row_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\ud83d\udc41\ufe0f"),jsx(RadixThemesButton,{css:({ ["padding"] : "0", ["fontSize"] : "1rem", ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.edit_record", ({ ["record_id"] : row_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u270f\ufe0f")))))))
    )
});
